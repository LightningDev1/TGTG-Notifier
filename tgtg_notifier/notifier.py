"""
Notifier module that checks TGTG for new items
"""

import time
import logging
from typing import List, NoReturn

from tgtg import TgtgClient

from config import Config
from telegram_bot.bot import TelegramBot
from discord_webhook.webhook import DiscordWebhook
from tgtg_notifier.items import Item, Items


class Notifier:
    "Notifier class that checks TGTG for new items"

    def __init__(
        self,
        config: Config,
        tgtg_client: TgtgClient,
        telegram_bot: TelegramBot,
        discord_webhook: DiscordWebhook,
    ) -> None:
        self.config = config
        self.tgtg_client = tgtg_client
        self.telegram_bot = telegram_bot
        self.discord_webhook = discord_webhook

        self.old_items = Items([])

    def get_new_items(self) -> List[Item]:
        "Get new items since last check"

        items = Items(self.tgtg_client.get_items())
        new_items = items.get_new_items(self.old_items)
        self.old_items = items
        return new_items

    def send_message(self, message: str) -> None:
        "Send a message to all enabled notification methods"

        if self.config.telegram_enabled:
            self.telegram_bot.send_message(message)

        if self.config.discord_enabled:
            if self.config.discord_mention:
                message = f"@everyone {message}"
            self.discord_webhook.send_message(message)

    def start_checking(self) -> NoReturn:
        "Start checking for new items"

        logging.info("Checking for new items")

        while True:
            try:
                self.config.load()
                new_items = self.get_new_items()
                for item in new_items:
                    message = self.config.message.format(item)
                    logging.info(message)
                    self.send_message(message)
            except Exception as exception:  # pylint: disable=broad-except
                logging.error("An error occurred: %s", exception, exc_info=True)
            finally:
                time.sleep(self.config.check_interval)
