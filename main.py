# main.py
# Главный файл бота - точка входа

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Импортируем конфигурацию и обработчики
from config import BOT_TOKEN
from handlers import routers


async def main():
    """
    Основная функция запуска бота.
    """
    # Настройка логирования (для отладки и мониторинга)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Запуск бота...")
    
    # Создаём бота с токеном
    # DefaultBotProperties позволяет установить параметры по умолчанию
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создаём диспетчер (обработчик событий)
    dp = Dispatcher()
    
    # Регистрируем все роутеры (обработчики команд)
    for router in routers:
        dp.include_router(router)
    
    logger.info("✅ Все обработчики зарегистрированы")
    
    try:
        # Удаляем старые обновления (webhook) перед запуском
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("📡 Бот начал получать обновления")
        
        # Запускаем бота в режиме polling (опрос сервера на новые сообщения)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        # Закрываем сессию бота при завершении
        await bot.session.close()
        logger.info("👋 Бот остановлен")


if __name__ == '__main__':
    """
    Точка входа в программу.
    Запускаем асинхронную функцию main()
    """
    try:
        # Запускаем event loop с основной функцией
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")

