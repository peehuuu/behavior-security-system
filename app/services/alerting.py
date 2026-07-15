# app/services/alerting.py
import logging

security_logger = logging.getLogger("security")


def send_alert(session_dict, user):
    """
    Stub alert dispatcher. In a real deployment, replace the body of this
    function with a call to an email API (e.g. SendGrid), a Slack/Discord
    webhook, or an SMS gateway. Keeping it as a single function means the
    detection code never needs to know or care which channel is used.
    """
    message = (
        f"[SENTINEL ALERT] user={user.username} risk={session_dict['risk_score']} "
        f"reasons={session_dict['reasons']}"
    )
    security_logger.critical(message)
    # Example of what a real webhook call would look like (left commented intentionally):
    # import requests
    # requests.post(WEBHOOK_URL, json={"text": message}, timeout=5)
    return message