"""Custom filters."""
import typing

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.builtin import HashTag


def register_filters(dp: Dispatcher):

    dp.filters_factory.bind(ChatTypeFilter,
            event_handlers=[dp.callback_query_handlers, dp.message_handlers])
    dp.filters_factory.bind(TextUnequalFilter,
                            event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsReplyToForwardFilter,
                            event_handlers=[dp.message_handlers])


class ChatTypeFilter(BoundFilter):
    """Check chat type."""
    key = 'chat_type'

    def __init__(self, chat_type: typing.Union[typing.Iterable, str]):
        if isinstance(chat_type, str):
            chat_type = [chat_type]
        self.chat_type = chat_type

    async def check(self,
            obj: typing.Union[types.CallbackQuery, types.Message]) -> bool:
        return obj.chat.type in self.chat_type


class TextUnequalFilter(BoundFilter):
    """Check text unequal."""
    key = 'text_unequal'

    def __init__(self, text_unequal: typing.Union[typing.Iterable, str]):
        if isinstance(text_unequal, str):
            text_unequal = [text_unequal]
        self.text_unequal = text_unequal

    async def check(self, message: types.Message) -> bool:
        return message.text not in self.text_unequal


class IsReplyToForwardFilter(BoundFilter):
    """
    Check if message is replied to forward and send reply message to
    handler.
    """
    key = 'is_reply_to_forward'

    def __init__(self, is_reply_to_forward: bool):
        self.is_reply_to_forward = is_reply_to_forward

    async def check(self, message: types.Message):
        if message.reply_to_message.forward_from and self.is_reply_to_forward:
            return True
        elif not message.reply_to_message.forward_from and\
                not self.is_reply_to_forward:
            return True


class ReplyHashTag(HashTag):
    """
    Checking for the presence of a hashtag in a reply to a message.
    """
    async def check(self, message: types.Message):
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption
            entities = message.reply_to_message.caption_entities
        elif message.reply_to_message.text:
            text = message.reply_to_message.text
            entities = message.reply_to_message.entities
        else:
            return False

        hashtags, cashtags = self._get_tags(text, entities)
        if self.hashtags and set(hashtags) & set(self.hashtags) \
                or self.cashtags and set(cashtags) & set(self.cashtags):
            return {'hashtags': hashtags, 'cashtags': cashtags}
