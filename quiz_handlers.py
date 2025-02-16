import asyncio
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from quiz_func import new_quiz, get_question
from quiz import quiz_data
from db_func import get_quiz_index, update_quiz_index
from aiogram import Dispatcher

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)

@dp.callback_query(lambda callback: callback.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery):

    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index, stat = await get_quiz_index(callback.from_user.id)

    #определяем ответ
    selected_index, correct_option_index = map(int, callback.data.split("_")[1:])
 
    selected_option = quiz_data[current_question_index]['options'][selected_index]
    right_option = quiz_data[current_question_index]['options'][correct_option_index]

    # Проверяем, правильный ли ответ
    if selected_index == correct_option_index:
        stat += 1
        await callback.message.answer(f"Правильно, это {selected_option}")
    else:
        await callback.message.answer(f"{selected_option} это неправильный ответ.\n Правильный ответ {right_option}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index, stat)

    await asyncio.sleep(2)
    
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer(f"Это был последний вопрос. Ваш результат {stat} из {len(quiz_data)} верных ответов.\n Квиз завершен!")