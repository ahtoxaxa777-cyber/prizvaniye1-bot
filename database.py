"""
База данных бота
Хранит пользователей, теги, email
"""

import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_file='bot.db'):
        self.db_file = db_file
    
    def init_db(self):
        """Создание таблиц БД"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                created_at TEXT,
                waiting_email INTEGER DEFAULT 0
            )
        ''')
        
        # Таблица тегов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                user_id INTEGER,
                tag TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username):
        """Добавить пользователя"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)',
            (user_id, username, datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
    
    def add_tag(self, user_id, tag):
        """Добавить тег пользователю"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Проверяем, нет ли уже такого тега
        cursor.execute('SELECT * FROM tags WHERE user_id = ? AND tag = ?', (user_id, tag))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO tags (user_id, tag, created_at) VALUES (?, ?, ?)',
                (user_id, tag, datetime.now().isoformat())
            )
        
        conn.commit()
        conn.close()
    
    def has_tag(self, user_id, tag):
        """Проверить наличие тега"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tags WHERE user_id = ? AND tag = ?', (user_id, tag))
        result = cursor.fetchone() is not None
        
        conn.close()
        return result
    
    def has_paid(self, user_id):
        """Проверить, оплатил ли пользователь"""
        return self.has_tag(user_id, 'paid')
    
    def save_email(self, user_id, email):
        """Сохранить email"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET email = ? WHERE user_id = ?', (email, user_id))
        
        conn.commit()
        conn.close()
    
    def set_waiting_email(self, user_id):
        """Установить флаг ожидания email"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET waiting_email = 1 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def is_waiting_email(self, user_id):
        """Проверить, ждём ли email"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT waiting_email FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result and result[0] == 1
    
    def clear_waiting_email(self, user_id):
        """Снять флаг ожидания email"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET waiting_email = 0 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_users_without_tag(self, tag):
        """Получить всех пользователей без определённого тега"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id FROM users
            WHERE user_id NOT IN (
                SELECT user_id FROM tags WHERE tag = ?
            )
        ''', (tag,))
        
        users = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return users
