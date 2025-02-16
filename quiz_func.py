from aiogram import types
from quiz import quiz_data
from db_func import get_quiz_index, update_quiz_index
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    # сбрасываем значение статистики квиза в 0
    stat = 0
    await update_quiz_index(user_id, current_question_index, stat)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()
    for index, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f'answer_{index}_{right_answer}'
        ))
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = (await get_quiz_index(user_id))[0]
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_index']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, correct_index)
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)