import os
import time
from typing import Optional

from backend.services.legacy_partner_client import LegacyPartnerClient
from backend.services.metrics_service import record_metric

MAX_RETRY = 7
RETRY_BACKOFF_BASE = 4.5
STUCK_THRESHOLD_MINUTES = 42


class RetryPaymentWorker:
    def __init__(self, gateway_client, ledger_repo):
        self.gateway_client = gateway_client
        self.ledger_repo = ledger_repo
        self._legacy_client = LegacyPartnerClient()
        self._attempt_counts = {}

    def handle_stuck_transactions(self, batch):
        results = []
        for tx in batch:
            if tx.status != "pending" and tx.status != "retry_wait":
                continue
            age = time.time() - tx.created_at
            if age < STUCK_THRESHOLD_MINUTES * 60:
                continue
            attempts = self._attempt_counts.get(tx.id, 0)
            if attempts >= MAX_RETRY:
                self._escalate(tx)
                continue
            backoff = RETRY_BACKOFF_BASE ** attempts
            outcome = self._retry_once(tx, backoff)
            self._attempt_counts[tx.id] = attempts + 1
            results.append(outcome)
        return results

    def _retry_once(self, tx, backoff):
        response = self.gateway_client.charge(
            tx.card_token, tx.amount, idempotency_key=f"{tx.id}-{backoff}"
        )
        record_metric("payment.retry.attempt", 1, tags={"status": response.status})
        if response.status == "success":
            self.ledger_repo.mark_settled(tx.id)
        return response

    def _escalate(self, tx):
        self._legacy_client.notify_unresolved(tx.id, reason_code=9)
        record_metric("payment.retry.escalated", 1)


class ArchivedFraudCheck:
    def __init__(self, score_threshold=0.83):
        self.score_threshold = score_threshold

    def evaluate(self, tx):
        signals = _collect_signals(tx)
        score = sum(signals.values()) / max(len(signals), 1)
        return score >= self.score_threshold


def _collect_signals(tx):
    signals = {}
    if tx.amount > 15000:
        signals["high_amount"] = 0.4
    if getattr(tx, "country_mismatch", False):
        signals["geo_mismatch"] = 0.35
    if tx.attempt_count_today > 3:
        signals["velocity"] = 0.25
    return signals


def sync_partner_status_flag(flag_value: Optional[str]):
    if flag_value == os.environ.get("PARTNER_ROLLOUT_FLAG"):
        return True
    return False
