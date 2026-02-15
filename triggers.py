"""
Система триггеров (добивок)
Отправляет сообщения с задержкой
"""

import asyncio
from aiogram import Bot
from config import (
    TRIGGER_1_DELAY, TRIGGER_2_DELAY, TRIGGER_3_DELAY, 
    TRIGGER_4_DELAY, TRIGGER_5_DELAY
)
from texts import TEXTS
from keyboards import get_trigger_keyboard

# Хранилище активных триггеров (чтобы можно было остановить)
active_triggers = {}


async def send_trigger(bot: Bot, user_id: int, trigger_num: int, delay: int, db):
    """Отправить один триггер с задержкой"""
    try:
        # Ждём заданное время
        await asyncio.sleep(delay)
        
        # Проверяем, не оплатил ли пользователь за это время
        if db.has_paid(user_id):
            return  # Если оплатил - не отправляем
        
        # Отправляем триггер
        trigger_text = TEXTS[f"trigger_{trigger_num}"]
        await bot.send_message(
            user_id,
            trigger_text,
            reply_markup=get_trigger_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Ошибка отправки триггера {trigger_num} пользователю {user_id}: {e}")


async def start_triggers(bot: Bot, user_id: int, db):
    """Запустить все триггеры для пользователя"""
    # Создаём задачи для всех триггеров
    tasks = [
        asyncio.create_task(send_trigger(bot, user_id, 1, TRIGGER_1_DELAY, db)),
        asyncio.create_task(send_trigger(bot, user_id, 2, TRIGGER_2_DELAY, db)),
        asyncio.create_task(send_trigger(bot, user_id, 3, TRIGGER_3_DELAY, db)),
        asyncio.create_task(send_trigger(bot, user_id, 4, TRIGGER_4_DELAY, db)),
        asyncio.create_task(send_trigger(bot, user_id, 5, TRIGGER_5_DELAY, db)),
    ]
    
    # Сохраняем задачи чтобы можно было остановить
    active_triggers[user_id] = tasks


def stop_triggers(user_id: int):
    """Остановить триггеры для пользователя (при оплате)"""
    if user_id in active_triggers:
        for task in active_triggers[user_id]:
            task.cancel()
        del active_triggers[user_id]
