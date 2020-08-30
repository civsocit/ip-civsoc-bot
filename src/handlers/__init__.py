from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import IDFilter
from aiogram.types import CallbackQuery

from config import DIRECTORS_CHAT, REDACTION_CHAT
from filters import ReplyHashTag
from states import Contact

from .about_fraction import about_fraction
from .directors_contact_directors_side import directors_reply
from .directors_contact_user_side import directors_state, set_directors_state
from .redaction_contact_redaction_side import redaction_reply
from .redaction_contact_user_side import redaction_state, set_redaction_state
from .start import start_cmd, start_cq, start_new_cq


def register_handlers(dp: Dispatcher):
    """
    Registration of all handlers.

    State handlers should be superior to others in their category.
    
    Order of categories:
    Callback queries handlers
    Commands handlers
    Messages handlers
    """
    # Start handlers by callback queries
    dp.register_callback_query_handler(start_cq, text='start', state='*')
    dp.register_callback_query_handler(start_new_cq, text='start_new', state='*')

    # When user click on button 'О фракции'
    dp.register_callback_query_handler(about_fraction, text='about_fraction')
    
    # When user click on button 'Связаться с директоратом'
    dp.register_callback_query_handler(set_directors_state, text='directors')

    # When user click on button 'Связаться с редакцией'
    dp.register_callback_query_handler(set_redaction_state, text='redaction')

    # Временная заглушка для неработающих функций
    dp.register_callback_query_handler(unavailable, text='unavailable')
    
    # Start handler by command
    dp.register_message_handler(start_cmd, chat_type='private', commands='start',
                                state='*')
    
    # When user send message for directors
    dp.register_message_handler(directors_state, state=Contact.directors)
    dp.register_message_handler(directors_state,
                                ReplyHashTag(hashtags='Директорат'),
                                chat_type='private', is_reply=True, state='*')

    # When user send message for redaction
    dp.register_message_handler(redaction_state, state=Contact.redaction)
    dp.register_message_handler(redaction_state,
                                ReplyHashTag(hashtags='Редакция'),
                                chat_type='private', is_reply=True, state='*')

    # When director replied to message from user
    dp.register_message_handler(directors_reply,
                                IDFilter(chat_id=DIRECTORS_CHAT),
                                text_unequal='.',
                                is_reply_to_forward=True)
    
    # When redactor replied to message from user
    dp.register_message_handler(redaction_reply,
                                IDFilter(chat_id=REDACTION_CHAT),
                                text_unequal='.',
                                is_reply_to_forward=True)


async def unavailable(cq: CallbackQuery):
    """Временная заглушка для неработающих функций."""
    await cq.answer('Эта функция пока не доступна.')
