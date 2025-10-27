# database/db.py
# Модуль для работы с базой данных SQLite3

import sqlite3
import csv
from datetime import datetime
from typing import List, Tuple, Optional


class Database:
    """
    Класс для работы с базой данных задач.
    """
    
    def __init__(self, db_path: str):
        """
        Инициализация подключения к базе данных.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """
        Создание таблицы tasks, если её ещё не существует.
        Таблица содержит поля:
        - id: уникальный идентификатор задачи (автоинкремент)
        - text: текст задачи
        - user: имя пользователя, создавшего задачу
        - created_at: дата и время создания задачи
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_task(self, text: str, user: str) -> int:
        """
        Добавление новой задачи в базу данных.
        
        Args:
            text: Текст задачи
            user: Имя пользователя
            
        Returns:
            ID добавленной задачи
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)',
                (text, user, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_tasks(self) -> List[Tuple]:
        """
        Получение всех задач из базы данных.
        
        Returns:
            Список кортежей (id, text, user, created_at)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, text, user, created_at FROM tasks ORDER BY created_at DESC')
            return cursor.fetchall()
    
    def export_to_csv(self, csv_path: str) -> bool:
        """
        Экспорт всех задач в CSV-файл.
        
        Args:
            csv_path: Путь к файлу для сохранения
            
        Returns:
            True если экспорт успешен, False в противном случае
        """
        try:
            tasks = self.get_all_tasks()
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Записываем заголовки
                writer.writerow(['ID', 'Задача', 'Пользователь', 'Дата создания'])
                # Записываем задачи
                writer.writerows(tasks)
            
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")
            return False
    
    def get_task_count(self) -> int:
        """
        Получение общего количества задач.
        
        Returns:
            Количество задач в базе данных
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM tasks')
            return cursor.fetchone()[0]

