"""
TGTG Notifier main module
"""

import logging

from tgtg import TgtgClient

from config import Config
from telegram_bot.bot import TelegramBot
from discord_webhook.webhook import DiscordWebhook
from tgtg_notifier.notifier import Notifier

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s -  %(message)s"
)

logging.info("Starting TGTG Notifier")

config = Config("config.json")

tgtg_client = TgtgClient(
    access_token=config.tgtg_access_token,
    refresh_token=config.tgtg_refresh_token,
    user_id=config.tgtg_user_id,
)

telegram_bot = TelegramBot(config, tgtg_client)
if config.telegram_enabled:
    telegram_bot.run()

discord_webhook = DiscordWebhook(config)

notifier = Notifier(config, tgtg_client, telegram_bot, discord_webhook)

notifier.start_checking()
