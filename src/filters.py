"""Custom filters."""
import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter


def register_filters(dp: Dispatcher):
    dp.filters_factory.bind(ChatTypeFilter,
            event_handlers=[dp.callback_query_handlers, dp.message_handlers])


class ChatTypeFilter(BoundFilter):
    key = 'chat_type'

    def __init__(self, chat_type: typing.Union[typing.Iterable, str]):
        if isinstance(chat_type, str):
            chat_type = [chat_type]
        self.chat_type = chat_type

    async def check(self,
            obj: typing.Union[types.CallbackQuery, types.Message]) -> bool:
        return obj.chat.type in self.chat_type
