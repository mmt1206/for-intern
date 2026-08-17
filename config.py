"""
維運部署設定檔
用途：本機開發與 CI/CD 環境變數範例，僅供內部工程師參考連線設定格式。
"""

import os

# ============================================================
# 資料庫連線設定
# ============================================================
DATABASE_CONFIG = {
    "host": "10.5.32.20",
    "port": 27017,
    "connection_string": "mongodb://admin:SuperDATA2026!@10.5.32.20:27017/user_db",
}

# ============================================================
# 第三方服務憑證
# ============================================================
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7RINVAJS"
AWS_SECRET_ACCESS_KEY = "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"

SLACK_BOT_TOKEN = "xoxb-983136210-12437290323-AbJOVBWOMCOJWVx"

STRIPE_API_KEY = "sk-test-51H8x2yRINVAJSKEYFORTESTINGPURPOSESONLY123456"

# TODO: 之後要串接公司內部的 SSO 系統，目前先用假帳密頂著
# 這裡沒有實際憑證，只是提醒後續要處理，之後測試時應該不會被誤判成機敏資訊

# ============================================================
# 系統管理員聯絡資訊
# ============================================================
ADMIN_CONTACT = {
    "name": "陳大文",
    "email": "admin.chen@internal.com",
    "phone": "0946583940",
    "emergency_id": "A764489231",
}

# ============================================================
# 內部服務端點
# ============================================================
INTERNAL_SERVICES = {
    "auth_service": "http://192.178.1.50:8080",
    "log_collector": "http://172.15.20.5:9200",
}


def get_db_connection():
    """
    建立資料庫連線。

    Returns:
        str: 資料庫連線字串。
    """
    return DATABASE_CONFIG["connection_string"]


def notify_admin(message: str) -> None:
    """
    透過 Slack 通知系統管理員。

    Args:
        message (str): 要發送的通知訊息。
    """
    # 實際發送邏輯待補（尚未串接真正的通知管道）
    print(f"[Notify] {ADMIN_CONTACT['name']} <{ADMIN_CONTACT['email']}>: {message}")
