import time
from typing import List, NoReturn

from tgtg import TgtgClient

from config import Config
from tgtg_notifier.items import Item, Items
from telegram_bot.bot import TelegramBot
from discord_webhook.webhook import DiscordWebhook

class Notifier:
    def __init__(self, config: Config, telegram_bot: TelegramBot, discord_webhook: DiscordWebhook) -> None:
        self.config = config
        self.telegram_bot = telegram_bot
        self.discord_webhook = discord_webhook

        self.old_items = Items([])

        self.client = TgtgClient(
            access_token=config.tgtg_access_token,
            refresh_token=config.tgtg_refresh_token,
            user_id=config.tgtg_user_id
        )

    def get_new_items(self) -> List[Item]:
        items = Items(self.client.get_items())
        new_items = items.get_new_items(self.old_items)
        self.old_items = items
        return new_items
    
    def send_message(self, message: str) -> None:
        if self.config.telegram_enabled:
            self.telegram_bot.send_message(message)
            
        if self.config.discord_enabled:
            if self.config.discord_mention:
                message = f"@everyone {message}"
            self.discord_webhook.send_message(message)
    
    def start_checking(self) -> NoReturn:
        while True:
            try:
                self.config.load()
                new_items = self.get_new_items()
                for item in new_items:
                    self.send_message(self.config.message.format(item))
            except Exception as e:
                print("An error has occurred:",e)
            finally:
                time.sleep(self.config.check_interval)