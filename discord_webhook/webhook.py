import requests

from config import Config

class DiscordWebhook:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.url = self.config.discord_webhook_url

    def send_message(self, message):
        requests.post(self.url, json={
            "content": message,
            "username": "TGTG Notifier",
            "avatar_url": "https://s3-eu-west-1.amazonaws.com/tgtg-mkt-cms-staging/306/sF6L9I02wgeMQAfOc3lRIaOqbuNpneQmZ28FwGOD.png"
        })