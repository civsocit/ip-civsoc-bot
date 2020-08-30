from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from config import DIRECTORS_CHAT
from filters import ReplyHashTag
from states import Contact

from .directors_contact_directors_side import directors_reply
from .directors_contact_user_side import directors_state, set_directors_state
from .start import start_cmd, start_cq, start_new_cq


def register_handlers(dp: Dispatcher):

    # Start handlers by callback queries
    dp.register_callback_query_handler(start_cq, text='start', state='*')
    dp.register_callback_query_handler(start_new_cq, text='start_new', state='*')

    # When user click on button 'Связаться с директоратом'
    dp.register_callback_query_handler(set_directors_state, text='directors')

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

    # When director replied to message from user
    dp.register_message_handler(directors_reply, text_unequal='.',
                                is_reply_to_forward=True,
                                chat_id=DIRECTORS_CHAT)


async def unavailable(cq: CallbackQuery):
    """Временная заглушка для неработающих функций."""
    await cq.answer('Эта функция пока не доступна.')
