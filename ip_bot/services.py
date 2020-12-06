from aiogram.types import Message, MessageEntityType


def get_ids_from_text_mentions(message: Message):
    ids = []
    for entity in message.entities:
            if entity.type == MessageEntityType.TEXT_MENTION:
                ids.append(entity.user.id)
    return ids
