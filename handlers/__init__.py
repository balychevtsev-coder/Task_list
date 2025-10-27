# handlers/__init__.py
# Инициализация пакета handlers

from .start import router as start_router
from .add_task import router as add_task_router
from .list_tasks import router as list_tasks_router

# Список всех роутеров для регистрации в главном файле
routers = [start_router, add_task_router, list_tasks_router]

__all__ = ['routers']

