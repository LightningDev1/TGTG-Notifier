"""
Configuration stuff
"""

import json
from os import path
from typing import List


class Config:
    "Config helper class with getters and setters for the config values"

    def __init__(self, file_path) -> None:
        if not path.exists(file_path):
            raise FileNotFoundError("Config file not found")

        self.file_path = file_path

        self.load()

    def load(self) -> None:
        "Load the config from the file"
        with open(self.file_path, "r", encoding="utf-8") as config_file:
            self.json = json.load(config_file)

    def save(self) -> None:
        "Save the config to the file"
        with open(self.file_path, "w", encoding="utf-8") as config_file:
            json.dump(self.json, config_file, indent=4)

    # Too Good To Go config
    @property
    def tgtg_access_token(self) -> str:
        "Too Good To Go API access token"
        return self.json["tgtg"]["access_token"]

    @tgtg_access_token.setter
    def tgtg_access_token(self, value: str):
        self.json["tgtg"]["access_token"] = value

    @property
    def tgtg_refresh_token(self) -> str:
        "Too Good To Go API refresh token"
        return self.json["tgtg"]["refresh_token"]

    @tgtg_refresh_token.setter
    def tgtg_refresh_token(self, value: str):
        self.json["tgtg"]["refresh_token"] = value

    @property
    def tgtg_user_id(self) -> str:
        "Too Good To Go API user ID"
        return self.json["tgtg"]["user_id"]

    @tgtg_user_id.setter
    def tgtg_user_id(self, value: str):
        self.json["tgtg"]["user_id"] = value

    # Telegram config
    @property
    def telegram_enabled(self) -> bool:
        "Telegram notifications enabled"
        return self.json["telegram"]["enabled"]

    @telegram_enabled.setter
    def telegram_enabled(self, value: bool):
        self.json["telegram"]["enabled"] = value

    @property
    def telegram_bot_token(self) -> str:
        "Telegram API bot token"
        return self.json["telegram"]["bot_token"]

    @telegram_bot_token.setter
    def telegram_bot_token(self, value: str):
        self.json["telegram"]["bot_token"] = value

    @property
    def telegram_chat_ids(self) -> List[int]:
        "Telegram chat IDs to send notifications to"
        return self.json["telegram"]["chat_ids"]

    @telegram_chat_ids.setter
    def telegram_chat_ids(self, value: List[int]):
        self.json["telegram"]["chat_ids"] = value

    # Discord config
    @property
    def discord_enabled(self) -> bool:
        "Discord notifications enabled"
        return self.json["discord"]["enabled"]

    @discord_enabled.setter
    def discord_enabled(self, value: bool):
        self.json["discord"]["enabled"] = value

    @property
    def discord_webhook_url(self) -> str:
        "Discord webhook URL"
        return self.json["discord"]["webhook_url"]

    @discord_webhook_url.setter
    def discord_webhook_url(self, value: str):
        self.json["discord"]["webhook_url"] = value

    @property
    def discord_avatar_url(self) -> str:
        "Discord avatar URL"
        return self.json["discord"]["avatar_url"]

    @discord_avatar_url.setter
    def discord_avatar_url(self, value: str):
        self.json["discord"]["avatar_url"] = value

    @property
    def discord_username(self) -> str:
        "Discord username"
        return self.json["discord"]["username"]

    @discord_username.setter
    def discord_username(self, value: str):
        self.json["discord"]["username"] = value

    @property
    def discord_mention(self) -> bool:
        "mention @everyone in Discord notifications"
        return self.json["discord"]["mention"]

    @discord_mention.setter
    def discord_mention(self, value: bool):
        self.json["discord"]["mention"] = value

    # General config
    @property
    def check_interval(self) -> int:
        "Interval in seconds to check for new items"
        return self.json["check_interval"]

    @check_interval.setter
    def check_interval(self, value: int):
        self.json["check_interval"] = value

    @property
    def message(self) -> str:
        "Message to send with the notification"
        return self.json["message"]

    @message.setter
    def message(self, value: str):
        self.json["message"] = value
