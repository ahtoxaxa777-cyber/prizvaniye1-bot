"""
Клавиатуры (кнопки) бота
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    NOTION_MODULE0, NOTION_MODULE1, NOTION_MODULE2, NOTION_MODULE3, NOTION_MODULE4, NOTION_MODULE5,
    NOTION_MODULE6, NOTION_MODULE7, NOTION_MODULE8, NOTION_MODULE9, NOTION_MODULE10,
    COMMUNITY_LINK
)


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Получить Модуль 1 (бесплатно)", callback_data="get_module1")],
        [InlineKeyboardButton(text="❓ Что это вообще такое?", callback_data="what_is_this")]
    ])
    return keyboard


def get_module1_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Открыть Модуль", url=NOTION_MODULE0)],
        [InlineKeyboardButton(text="💳 Купить полный курс (9,900₽)", callback_data="buy_course")]
    ])
    return keyboard


def get_buy_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Получить Модуль 1", callback_data="get_module1")],
        [InlineKeyboardButton(text="💳 Купить сразу (9,900₽)", callback_data="buy_course")]
    ])
    return keyboard


def get_trigger_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить полный курс (9,900₽)", callback_data="buy_course")],
        [InlineKeyboardButton(text="📚 Посмотреть все модули", callback_data="show_modules")]
    ])
    return keyboard


def get_modules_keyboard(paid=False):
    """Кнопки списка модулей"""
    if not paid:
        # Для неоплативших
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Модуль 0: Проблема (бесплатно)", url=NOTION_MODULE0)],
        [InlineKeyboardButton(text="🔒 Модуль 1: Начало пути", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модуль 2: Диагностика", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модуль 3: Анализ прошлого", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модуль 4: Суперсилы", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модуль 5: Реальность рынка", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модуль 6: Первые шаги", callback_data="locked")],
        [InlineKeyboardButton(text="🔒 Модули 7-10: Скоро", callback_data="locked")],
        [InlineKeyboardButton(text="💳 Купить полный курс (9,900₽)", callback_data="buy_course")]
        ])
    else:
        # Для оплативших - все модули
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Модуль 1: Проблема", url=NOTION_MODULE1)],
            [InlineKeyboardButton(text="✅ Модуль 2: Диагностика", url=NOTION_MODULE2)],
            [InlineKeyboardButton(text="✅ Модуль 3: Анализ прошлого", url=NOTION_MODULE3)],
            [InlineKeyboardButton(text="✅ Модуль 4: Ценности и таланты", url=NOTION_MODULE4)],
            [InlineKeyboardButton(text="✅ Модуль 5: Гипотезы призвания", url=NOTION_MODULE5)],
            [InlineKeyboardButton(text="✅ Модуль 6: Тестирование", url=NOTION_MODULE6)],
            [InlineKeyboardButton(text="✅ Модуль 7: Формулирование миссии", url=NOTION_MODULE7)],
            [InlineKeyboardButton(text="✅ Модуль 8: План на 90 дней", url=NOTION_MODULE8)],
            [InlineKeyboardButton(text="✅ Модуль 9: Интеграция в жизнь", url=NOTION_MODULE9)],
            [InlineKeyboardButton(text="✅ Модуль 10: Твой путь начинается", url=NOTION_MODULE10)],
            [InlineKeyboardButton(text="👥 Закрытое комьюнити", url=COMMUNITY_LINK)]
        ])
    
    return keyboard
