# актоивация виртуального окружения и установка библиотек, прописывается в терминале
# # python -m venv .venv
# .venv\Scripts\activate
#pip install aiogram
#pip install aiosqlite

#### после окончания работы не забыть pip freeze > requirements.txt ###

import asyncio
import logging
from aiogram import Bot
from db_func import create_table
from quiz_handlers import dp

try:
    from API_TOKEN import YOUR_BOT_TOKEN
except ImportError:
    print('Для использования бота необходим API ключ для управления ботом')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен в кавычках, который вы получили от BotFather
API_TOKEN = YOUR_BOT_TOKEN

# Объект бота
bot = Bot(token=API_TOKEN)

# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())