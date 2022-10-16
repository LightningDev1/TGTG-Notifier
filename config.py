import json
from os import path
from typing import List

class Config:
    def __init__(self, file_path) -> None:
        if not path.exists(file_path):
            raise FileNotFoundError("Config file not found")

        self.file_path = file_path

        self.load()
    
    def load(self) -> None:
        with open("config.json", "r") as f:
            self.json = json.load(f)
    
    def save(self) -> None:
        with open("config.json", "w") as f:
            json.dump(self.json, f, indent=4)
    
    # Too Good To Go config
    @property
    def tgtg_access_token(self) -> str:
        return self.json["tgtg"]["access_token"]
    @tgtg_access_token.setter
    def tgtg_access_token(self, value: str):
        self.json["tgtg"]["access_token"] = value
    
    @property
    def tgtg_refresh_token(self) -> str:
        return self.json["tgtg"]["refresh_token"]
    @tgtg_refresh_token.setter
    def tgtg_refresh_token(self, value: str):
        self.json["tgtg"]["refresh_token"] = value
    
    @property
    def tgtg_user_id(self) -> str:
        return self.json["tgtg"]["user_id"]
    @tgtg_user_id.setter
    def tgtg_user_id(self, value: str):
        self.json["tgtg"]["user_id"] = value
    
    # Telegram config
    @property
    def telegram_enabled(self) -> bool:
        return self.json["telegram"]["enabled"]
    @telegram_enabled.setter
    def telegram_enabled(self, value: bool):
        self.json["telegram"]["enabled"] = value

    @property
    def telegram_bot_token(self) -> str:
        return self.json["telegram"]["bot_token"]
    @telegram_bot_token.setter
    def telegram_bot_token(self, value: str):
        self.json["telegram"]["bot_token"] = value

    @property
    def telegram_chat_ids(self) -> List[int]:
        return self.json["telegram"]["chat_ids"]
    @telegram_chat_ids.setter
    def telegram_chat_ids(self, value: List[int]):
        self.json["telegram"]["chat_ids"] = value
    
    # Discord config
    @property
    def discord_enabled(self) -> bool:
        return self.json["discord"]["enabled"]
    @discord_enabled.setter
    def discord_enabled(self, value: bool):
        self.json["discord"]["enabled"] = value
    
    @property
    def discord_webhook_url(self) -> str:
        return self.json["discord"]["webhook_url"]
    @discord_webhook_url.setter
    def discord_webhook_url(self, value: str):
        self.json["discord"]["webhook_url"] = value
    
    @property
    def discord_mention(self) -> bool:
        return self.json["discord"]["mention"]
    @discord_mention.setter
    def discord_mention(self, value: bool):
        self.json["discord"]["mention"] = value
    
    # General config
    @property
    def check_interval(self) -> int:
        return self.json["check_interval"]
    @check_interval.setter
    def check_interval(self, value: int):
        self.json["check_interval"] = value
    
    @property
    def message(self) -> str:
        return self.json["message"]
    @message.setter
    def message(self, value: str):
        self.json["message"] = value