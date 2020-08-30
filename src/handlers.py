from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from config import DIRECTORS_CHAT
from filters import ReplyHashTag
import screens as scr
from states import Contact


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_cq, text='start', state='*')

    dp.register_callback_query_handler(start_new_cq, text='start_new', state='*')

    dp.register_callback_query_handler(set_directors_state, text='directors')

    dp.register_callback_query_handler(unavailable, text='unavailable')
    
    dp.register_message_handler(start_cmd, chat_type='private', commands='start',
                                state='*')
    
    dp.register_message_handler(directors_state, state=Contact.directors)

    dp.register_message_handler(directors_state,
                                ReplyHashTag(hashtags='Директорат'),
                                chat_type='private', is_reply=True, state='*')

    dp.register_message_handler(directors_reply, text_unequal='.',
                                is_reply_to_forward=True,
                                chat_id=DIRECTORS_CHAT)


async def start_cmd(message: types.Message, state: FSMContext):
    await state.finish()
    screen = scr.Start(message.from_user.first_name)
    await message.answer(**screen.as_dict())


async def start_cq(cq: types.CallbackQuery, state: FSMContext):
    await state.finish()
    screen = scr.Start(cq.from_user.first_name)
    await cq.message.edit_text(**screen.as_dict())


async def start_new_cq(cq: types.CallbackQuery, state=FSMContext):
    await state.finish()
    screen = scr.Start(cq.from_user.first_name)
    await cq.message.answer(**screen.as_dict())


async def set_directors_state(cq: types.CallbackQuery):
    await Contact.directors.set()
    await cq.message.edit_text(**scr.ContactDirectors().as_dict())


async def directors_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.forward(DIRECTORS_CHAT)
    screen = scr.MessageForwarded('директорату')
    await message.answer(**screen.as_dict())
    screen = scr.Start(message.from_user.first_name)
    await message.answer(**screen.as_dict())


async def directors_reply(message: types.Message):
    screen = scr.MessageFrom('Директорат', message.parse_entities())
    await message.bot.send_message(chat_id=message.reply_to_message.forward_from.id,
                                   **screen.as_dict())


async def unavailable(cq: types.CallbackQuery):
    await cq.answer('Эта функция пока не доступна.')
