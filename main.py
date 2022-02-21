import logging

import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from key import token
from aiogram.utils import executor

API_TOKEN = token

# Подключаем соответствующую конфигурацию логгирования документа
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры классов Bot и Dispatcher, которые мы заранее ипортировали
# из библиотеки aiogram на строке 2
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


# import os
# print(os.listdir("."))

async def on_startup(_):
    logging.info("Bot was started")


@dp.message_handler(commands=['to_bot'])
@dp.message_handler(Text(contains='вопрос боту'))
async def get_question(message: types.Message):
    fsa = "lednev_bot\\service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Microelectronics")

    wsh = sh.worksheet('Data')

    try:
        wsh.append_row([message.chat.id, message.from_user.id, message.from_user.username, message.text,
                        message.from_user.full_name])
        await message.reply('Ваш вопрос добавлен в общий список вопросов. Спасибо.')
    except:
        await message.reply('Не удалось зафиксировать Ваш вопрос, просьба направить его почтой, спасибо!')


# def register_bot_handlers(pp: Dispatcher):

# pp.register_message_handler(get_question, text=['вопрос боту'], ignore_case=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
