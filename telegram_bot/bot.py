"""
Telegram bot for sending notifications
"""

import asyncio
import logging
import threading
import multiprocessing
import platform
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config


class TelegramBot:
    "Telegram bot class"

    def __init__(self, config: Config):
        self.config = config
        self.token = self.config.telegram_bot_token

        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))

        # threading does not seem to work on Linux, while multiprocessing does not work on Windows
        # so just check what platform we're running on and use the correct one
        if platform.system() == "Windows":
            self.thread = threading.Thread(target=self._run, daemon=True)
        else:
            self.thread = multiprocessing.Process(target=self._run, daemon=True)

    async def start(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        "/start command handler"

        self.config.load()
        chat_ids = self.config.telegram_chat_ids

        if update.message.chat_id not in chat_ids:
            chat_ids.append(update.message.chat_id)
            self.config.telegram_chat_ids = chat_ids
            self.config.save()
            logging.info(
                "Added new Telegram chat ID: %s username: %s",
                update.message.chat_id,
                update.message.chat.username,
            )

        await update.message.reply_html("TGTG Notifier ready!")

    def send_message(self, message):
        "Send a message to every Telegram chat ID"

        for chat_id in self.config.telegram_chat_ids:
            requests.get(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                params={
                    "chat_id": chat_id,
                    "text": message,
                },
            )

    def _run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.application.run_polling()

    def run(self):
        "Start the bot"

        self.thread.start()
