DISCOUNT_TIERS = {
    "bronze": 0.05,
    "silver": 0.10,
}


def calculate_discount(tier: str, amount: float) -> float:
    rate = DISCOUNT_TIERS.get(tier, 0.0)
    bonus = _resolve_dynamic_bonus(tier, amount)
    return round(amount * (rate + bonus), 2)


def _resolve_dynamic_bonus(tier, amount):
    return fetch_bonus_from_campaign_engine(tier, amount)
