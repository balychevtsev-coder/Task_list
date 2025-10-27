# handlers/list_tasks.py
# Обработчики команд /list и /list_csv для просмотра задач

import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from database import Database
from config import DATABASE_PATH

# Создаём роутер для обработки команд
router = Router()

# Инициализируем базу данных
db = Database(DATABASE_PATH)


@router.message(Command('list'))
async def cmd_list_tasks(message: Message):
    """
    Обработчик команды /list.
    Выводит все задачи из базы данных в виде текста.
    """
    try:
        # Получаем все задачи из базы данных
        tasks = db.get_all_tasks()
        
        # Проверяем, есть ли задачи
        if not tasks:
            await message.answer("📭 Список задач пуст.\n\nИспользуйте /add чтобы добавить задачу.")
            return
        
        # Формируем текст со списком задач
        tasks_text = f"📋 Всего задач: {len(tasks)}\n\n"
        
        for task in tasks:
            task_id, text, user, created_at = task
            # Форматируем дату (убираем миллисекунды)
            date = created_at.split('.')[0] if '.' in created_at else created_at
            
            tasks_text += (
                f"#{task_id} | 👤 @{user}\n"
                f"📝 {text}\n"
                f"📅 {date}\n"
                f"{'-' * 40}\n\n"
            )
        
        # Отправляем список задач
        # Если текст слишком длинный, Telegram разобьёт его на несколько сообщений
        await message.answer(tasks_text)
        
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при получении списка задач:\n{str(e)}")


@router.message(Command('list_csv'))
async def cmd_list_csv(message: Message):
    """
    Обработчик команды /list_csv.
    Создаёт CSV-файл со всеми задачами и отправляет его пользователю.
    """
    try:
        # Проверяем, есть ли задачи
        task_count = db.get_task_count()
        
        if task_count == 0:
            await message.answer("📭 Список задач пуст.\n\nИспользуйте /add чтобы добавить задачу.")
            return
        
        # Имя файла для экспорта
        csv_filename = 'tasks_export.csv'
        
        # Экспортируем задачи в CSV
        if db.export_to_csv(csv_filename):
            # Создаём объект файла для отправки
            file = FSInputFile(csv_filename)
            
            # Отправляем файл пользователю
            await message.answer_document(
                document=file,
                caption=f"📊 Экспорт задач в CSV\n\n"
                        f"Всего задач: {task_count}\n"
                        f"Формат: ID, Задача, Пользователь, Дата создания"
            )
            
            # Удаляем временный файл после отправки
            if os.path.exists(csv_filename):
                os.remove(csv_filename)
        else:
            await message.answer("❌ Не удалось создать CSV-файл.")
            
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при создании CSV:\n{str(e)}")
        
        # Удаляем файл в случае ошибки
        if os.path.exists('tasks_export.csv'):
            os.remove('tasks_export.csv')

