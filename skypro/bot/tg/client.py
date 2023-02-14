import requests
from requests import Response

from .dc import GetUpdatesResponse, SendMessagesResponse


class TgClient:
    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str) -> str:
        """
        Returns url to TG bot in str format with requested method
        """
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """
        Requests TG bot with getUpdates
        """
        url: str = self.get_url(method='getUpdates')
        response: Response = requests.get(url, params={'offset': offset, 'timeout': timeout})
        return GetUpdatesResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessagesResponse:
        """
        Requests TG bot with sendMessage
        """
        url: str = self.get_url('sendMessage')
        response: Response = requests.post(url, json={'chat_id': chat_id, 'text': text})
        return SendMessagesResponse(**response.json())
