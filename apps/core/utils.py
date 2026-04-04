from django.conf import settings
from .constants import (
    TEAMS_MESSAGE_TYPE,
    TEAMS_CONTENT_TYPE,
    TEAMS_CARD_TYPE,
    TEAMS_BLOCK_TYPE,
    TEAMS_SCHEMA,
    TEAMS_CARD_VERSION,
    POST
)
from .api_client import api_client

def send_message_to_teams(message: str) -> None:
    """
    Send a message to Teams channel.
    """
    if not settings.ENABLE_TEAMS_NOTIFICATIONS:
        return

    client = api_client()

    payload = {
        "type": TEAMS_MESSAGE_TYPE,
        "attachments": [
            {
                "contentType": TEAMS_CONTENT_TYPE,
                "content": {
                    "type": TEAMS_CARD_TYPE,
                    "body": [
                        {
                            "type": TEAMS_BLOCK_TYPE,
                            "text": message,
                        }
                    ],
                    "$schema": TEAMS_SCHEMA,
                    "version": TEAMS_CARD_VERSION,
                },
            }
        ],
    }

    client.call_api(
        endpoint=settings.TEAMS_WEBHOOK_URL,
        method=POST,
        data=payload,
    )