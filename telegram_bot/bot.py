"""
Telegram bot for sending notifications
"""

import asyncio
import logging
import threading
import multiprocessing
import platform
import requests

from tgtg import TgtgClient

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import prettytable as pt

from config import Config
from tgtg_notifier.items import Items
import utils


class TelegramBot:
    "Telegram bot class"

    def __init__(self, config: Config, tgtg_client: TgtgClient) -> None:
        self.config = config
        self.token = self.config.telegram_bot_token

        self.tgtg_client = tgtg_client

        # Intialize Telegram application
        self.application = Application.builder().token(self.token).build()

        # Add the command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("available", self.available))

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

    async def available(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        "/available command handler"

        ## Create a table with item name, price and quantity

        items = Items(self.tgtg_client.get_items()).get_items()

        # Sort the items so that the available ones are at the top
        items.sort(key=lambda item: item.available, reverse=True)

        table = pt.PrettyTable(["Item", "Price", "Stock"])
        table.align["Item"] = "c"
        table.align["Price"] = "c"
        table.align["Stock"] = "c"

        for item in items:
            table.add_row(
                [f"{item.store_name} ({item.name})", item.price, item.available]
            )

        ## Create an image from the table and send it to the user

        image = utils.prettytable_to_image(table)
        image_io = utils.image_to_io(image)

        await update.message.reply_photo(image_io)

    def send_message(self, message: str) -> None:
        "Send a message to every Telegram chat ID"

        for chat_id in self.config.telegram_chat_ids:
            requests.get(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                params={
                    "chat_id": chat_id,
                    "text": message,
                },
            )

    def _run(self) -> None:
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.application.run_polling()

    def run(self) -> None:
        "Start the bot"

        self.thread.start()
