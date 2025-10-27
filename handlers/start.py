# handlers/start.py
# Обработчик команды /start

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_kb import get_main_keyboard

# Создаём роутер для обработки команд
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.
    Приветствует пользователя и показывает доступные команды.
    """
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🤖 Я бот для управления задачами в команде.\n\n"
        "📋 Доступные команды:\n"
        "/add - Добавить новую задачу\n"
        "/list - Показать все задачи\n"
        "/list_csv - Получить список задач в формате CSV\n\n"
        "💡 Для добавления задачи используйте:\n"
        "/add Текст вашей задачи"
    )
    
    # Отправляем сообщение с клавиатурой
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

