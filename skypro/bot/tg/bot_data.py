from abc import ABC, abstractmethod
from enum import Enum


class Storage(ABC):
    @abstractmethod
    def get_state(self, chat_id: int) -> Enum | None:
        """Checks chat's state"""
        raise NotImplementedError

    @abstractmethod
    def get_data(self, chat_id: int) -> dict:
        """Gets chat_id from storage"""
        raise NotImplementedError

    @abstractmethod
    def set_state(self, chat_id: int, state: Enum) -> None:
        """Sets chat's state"""
        raise NotImplementedError

    @abstractmethod
    def set_data(self, chat_id: int, data: dict) -> None:
        """Sends chat_id and new goal to storage"""
        raise NotImplementedError

    @abstractmethod
    def reset(self, chat_id: int) -> bool:
        """Resets chat's data in storage"""
        raise NotImplementedError

    @abstractmethod
    def update_data(self, chat_id: int, **kwargs) -> None:
        """Updates exists chats data"""
        raise NotImplementedError
