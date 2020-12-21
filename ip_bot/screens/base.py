from typing import Union

from aiogram import Bot, types


class BaseScreen:
    fields = ['reply_markup']

    reply_markup: Union[
        types.InlineKeyboardMarkup,
        types.ReplyKeyboardMarkup,
        types.ReplyKeyboardRemove,
        types.ForceReply,
        None
    ] = None

    def __iter__(self):
        for field in self.fields:
            value = getattr(self, field)
            if value:
                yield field, value


class BaseTextScreen(BaseScreen):
    fields = ['text', 'disable_web_page_preview', 'reply_markup']

    text: str
    parse_mode: str = 'html'
    disable_web_page_preview: bool = False

    @classmethod
    async def send(cls, bot: Bot, chat_id: int,
                   disable_notification: bool = False,
                   **kwargs):
        screen = cls(**kwargs)
        return await bot.send_message(
            chat_id,
            disable_notification=disable_notification,
            **dict(screen)
        )

    @classmethod
    async def reply_to(cls, bot: Bot, chat_id: int, message_id: int,
                       disable_notification: bool = False,
                       **kwargs):
        screen = cls(**kwargs)
        return await bot.send_message(
            chat_id,
            disable_notification=disable_notification,
            reply_to_message_id=message_id,
            **dict(screen)
        )

    @classmethod
    async def edit(cls, bot: Bot, chat_id: int, message_id: int, **kwargs):
        screen = cls(**kwargs)
        return await bot.edit_message_text(chat_id=chat_id,
                                           message_id=message_id,
                                           **dict(screen))

    def as_dict(self) -> dict:
        return {'text': self.text,
                'disable_web_page_preview': self.disable_web_page_preview,
                'reply_markup': self.reply_markup}
