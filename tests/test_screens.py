import typing

import pytest
from aiogram import Bot, types
from aiogram.types import base

from ip_bot.screens.base import BaseScreen, BaseTextScreen


pytestmark = pytest.mark.asyncio


class FakeBot(Bot):
    def __init__(self):
        pass

    async def send_message(
        self,
        chat_id: typing.Union[base.Integer, base.String],
        text: base.String,
        parse_mode: typing.Optional[base.String] = None,
        entities: typing.Optional[typing.List[types.MessageEntity]] = None,
        disable_web_page_preview: typing.Optional[base.Boolean] = None,
        disable_notification: typing.Optional[base.Boolean] = None,
        reply_to_message_id: typing.Optional[base.Integer] = None,
        allow_sending_without_reply: typing.Optional[base.Boolean] = None,
        reply_markup: typing.Union[types.InlineKeyboardMarkup,
                                   types.ReplyKeyboardMarkup,
                                   types.ReplyKeyboardRemove,
                                   types.ForceReply, None] = None
    ) -> typing.Dict[str, typing.Any]:
        return {'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'entities': entities,
                'disable_web_page_preview': disable_web_page_preview,
                'disable_notification': disable_notification,
                'reply_to_message_id': reply_to_message_id,
                'allow_sending_without_reply': allow_sending_without_reply,
                'reply_markup': reply_to_message_id}

    async def edit_message_text(
        self,
        text: base.String,
        chat_id: typing.Union[base.Integer, base.String, None] = None,
        message_id: typing.Optional[base.Integer] = None,
        inline_message_id: typing.Optional[base.String] = None,
        parse_mode: typing.Optional[base.String] = None,
        entities: typing.Optional[typing.List[types.MessageEntity]] = None,
        disable_web_page_preview: typing.Optional[base.Boolean] = None,
        reply_markup: typing.Union[types.InlineKeyboardMarkup, None] = None,
    ) -> types.Message or base.Boolean:
        return {'text': text,
                'chat_id': chat_id,
                'message_id': message_id,
                'inline_message_id': inline_message_id,
                'parse_mode': parse_mode,
                'entities': entities,
                'disable_web_page_preview': disable_web_page_preview,
                'reply_markup': reply_markup}


class TestBaseScreen:
    def test_dict_with_reply_markup(self):
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton('qq', url='https://t.me/'))
        screen = BaseScreen()
        screen.reply_markup = reply_markup
        assert dict(screen) == {'reply_markup': reply_markup}

    def test_dict_without_values(self):
        screen = BaseScreen()
        assert dict(screen) == {}


class TestBaseTextScreen:
    async def test_send(self):
        text = 'Some string'
        bot = FakeBot()
        chat_id = 1

        class TextScreen(BaseTextScreen):
            def __init__(self):
                self.text = text
        result = await TextScreen.send(bot, chat_id)
        assert result['chat_id'] == chat_id
        assert result['text'] == text

    async def test_reply(self):
        text = 'Some string'
        bot = FakeBot()
        chat_id = 1
        message_id = 1

        class TextScreen(BaseTextScreen):
            def __init__(self):
                self.text = text
        result = await TextScreen.reply_to(bot, chat_id, message_id)
        assert result['chat_id'] == chat_id
        assert result['reply_to_message_id'] == message_id
        assert result['text'] == text

    async def test_edit(self):
        text = 'Some string'
        bot = FakeBot()
        chat_id = 1
        message_id = 1

        class TextScreen(BaseTextScreen):
            def __init__(self):
                self.text = text
        result = await TextScreen.edit(bot, chat_id, message_id)
        assert result['chat_id'] == chat_id
        assert result['message_id'] == message_id
        assert result['text'] == text
