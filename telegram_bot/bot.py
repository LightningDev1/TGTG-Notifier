import asyncio
import threading
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config

class TelegramBot:
    def __init__(self, config: Config):
        self.config = config
        self.token = self.config.telegram_bot_token

        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))

        self.process = threading.Thread(target=self._run, daemon=True)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.config.load()
        chat_ids = self.config.telegram_chat_ids

        if update.message.chat_id not in chat_ids:
            chat_ids.append(update.message.chat_id)
            self.config.telegram_chat_ids = chat_ids
            self.config.save()

        await update.message.reply_html("TGTG Notifier ready!")
    
    def send_message(self, message):
        for chat_id in self.config.telegram_chat_ids:
            requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage", params={
                "chat_id": chat_id,
                "text": message                
            })
    
    def _run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.application.run_polling()
    
    def run(self):
        self.process.start()