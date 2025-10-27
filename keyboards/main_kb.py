# keyboards/main_kb.py
# Клавиатуры для бота

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание основной клавиатуры с быстрыми командами.
    
    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками команд
    """
    # Создаём кнопки
    button_list = KeyboardButton(text="📋 Список задач")
    button_add = KeyboardButton(text="➕ Добавить задачу")
    button_csv = KeyboardButton(text="📊 Экспорт CSV")
    
    # Создаём клавиатуру
    # resize_keyboard=True - автоматическая подгонка размера кнопок
    # one_time_keyboard=False - клавиатура остаётся после нажатия
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_list, button_add],
            [button_csv]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие или введите команду..."
    )
    
    return keyboard

