from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

import screens as scr


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(unavailable, text='unavailable')
    dp.register_message_handler(start, chat_type='private', commands='start',
                                state='*')


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    scr.start['text'] = scr.start['text']\
            .format(name=message.from_user.first_name)
    await message.answer(**scr.start)


async def unavailable(cq: types.CallbackQuery):
    await cq.answer('Эта функция пока не доступна.')
