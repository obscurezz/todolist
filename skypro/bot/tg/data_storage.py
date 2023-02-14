from enum import Enum
from pydantic import BaseModel
from .bot_data import Storage


class StorageData(BaseModel):
    state: Enum | None = None
    data: dict = {}


class BotDataStorage(Storage):
    """Working with bot data"""
    def __init__(self):
        self.data: dict[int, StorageData] = {}

    def _resolve_chat(self, chat_id: int):
        """Checks if there is chat_id in storage. If not - creates one."""
        if chat_id not in self.data:
            self.data[chat_id] = StorageData()
        return self.data[chat_id]

    def get_state(self, chat_id: int) -> StorageData | None:
        """Checks chat's state"""
        return self._resolve_chat(chat_id).state

    def get_data(self, chat_id: int) -> dict:
        """Gets chat_id from storage"""
        return self._resolve_chat(chat_id).data

    def set_state(self, chat_id, state: Enum) -> None:
        """Sets chat's state"""
        self._resolve_chat(chat_id).state = state

    def set_data(self, chat_id: int, data: dict) -> None:
        """Sends chat_id and new goal to storage"""
        self._resolve_chat(chat_id).data = data

    def reset(self, chat_id: int) -> bool:
        """Resets chat's data in storage"""
        return bool(self.data.pop(chat_id, None))

    def update_data(self, chat_id: int, **kwargs) -> None:
        """Updates exists chats data"""
        self._resolve_chat(chat_id).data.update(**kwargs)
