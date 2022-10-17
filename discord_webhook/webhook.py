"""
Discord webhooks
"""

import requests

from config import Config


class DiscordWebhook:
    "Discord webhook helper class"

    def __init__(self, config: Config) -> None:
        self.config = config

    def send_message(self, message: str):
        "Send a message to the Discord webhook"

        requests.post(
            self.config.discord_webhook_url,
            json={
                "content": message,
                "username": self.config.discord_username,
                "avatar_url": self.config.discord_avatar_url,
            },
        )
