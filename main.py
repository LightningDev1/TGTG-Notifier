from config import Config
from telegram_bot.bot import TelegramBot
from discord_webhook.webhook import DiscordWebhook
from tgtg_notifier.notifier import Notifier

config = Config("config.json")

telegram_bot = TelegramBot(config)
if config.telegram_enabled:
    telegram_bot.run()

discord_webhook = DiscordWebhook(config)

notifier = Notifier(config, telegram_bot, discord_webhook)

notifier.start_checking()