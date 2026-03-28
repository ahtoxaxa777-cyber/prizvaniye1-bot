"""
Клавиатуры бота - ИСПРАВЛЕННАЯ ВЕРСИЯ
Добавлены: кнопка Назад, правильные названия модулей
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    NOTION_MODULE0, NOTION_MODULE1, NOTION_MODULE2, NOTION_MODULE3,
    NOTION_MODULE4, NOTION_MODULE5, NOTION_MODULE6, NOTION_MODULE7,
    NOTION_MODULE8, NOTION_MODULE9, NOTION_MODULE10,
    COMMUNITY_LINK
)


def get_start_keyboard():
    """Кнопки приветствия"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить Модуль 0 (бесплатно)", callback_data="get_module1")],
        [InlineKeyboardButton(text="Пройти диагностику — 1 490 ₽", callback_data="buy_diagnostic")],
        [InlineKeyboardButton(text="Что это такое?", callback_data="what_is_this")]
    ])


def get_module1_keyboard():
    """Кнопки после выдачи Модуля 0"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Модуль 0", url=NOTION_MODULE0)],
        [InlineKeyboardButton(text="Купить полный курс - 9 900 ₽", callback_data="buy_course")]
    ])


def get_buy_keyboard():
    """Кнопки покупки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить Модуль 0 бесплатно", callback_data="get_module1")],
        [InlineKeyboardButton(text="Купить курс сразу - 9 900 ₽", callback_data="buy_course")]
    ])


def get_back_to_start_keyboard():
    """Кнопка Назад - для экрана ввода email"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_start")]
    ])


def get_trigger_keyboard():
    """Кнопки в триггерах (добивках)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить полный курс - 9 900 ₽", callback_data="buy_course")],
        [InlineKeyboardButton(text="Посмотреть все модули", callback_data="show_modules")]
    ])


def get_modules_keyboard(paid=False):
    """
    Кнопки списка модулей.
    ИСПРАВЛЕНО: названия модулей теперь соответствуют реальной структуре курса.
    """
    if not paid:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Модуль 0: Почему 80% живут не своей жизнью (бесплатно)",
                url=NOTION_MODULE0
            )],
            [InlineKeyboardButton(text="Модуль 1: Что такое призвание - без мифов", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 2: Диагностика - где ты сейчас", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 3: Страхи и убеждения - что держит", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 4: Анализ прошлого - моменты потока", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 5: Ценности и суперсилы", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 6: Реальность рынка", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 7: Гипотеза и MVP", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 8: ИИ как усилитель призвания", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 9: Стратегия и первые клиенты", callback_data="locked")],
            [InlineKeyboardButton(text="Модуль 10: Система роста и масштаб", callback_data="locked")],
            [InlineKeyboardButton(text="Купить полный курс - 9 900 ₽", callback_data="buy_course")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Модуль 0: Лид-магнит", url=NOTION_MODULE0)],
            [InlineKeyboardButton(text="Модуль 1: Что такое призвание - без мифов", url=NOTION_MODULE1)],
            [InlineKeyboardButton(text="Модуль 2: Диагностика - где ты сейчас", url=NOTION_MODULE2)],
            [InlineKeyboardButton(text="Модуль 3: Страхи и убеждения - что держит", url=NOTION_MODULE3)],
            [InlineKeyboardButton(text="Модуль 4: Анализ прошлого - моменты потока", url=NOTION_MODULE4)],
            [InlineKeyboardButton(text="Модуль 5: Ценности и суперсилы", url=NOTION_MODULE5)],
            [InlineKeyboardButton(text="Модуль 6: Реальность рынка", url=NOTION_MODULE6)],
            [InlineKeyboardButton(text="Модуль 7: Гипотеза и MVP", url=NOTION_MODULE7)],
            [InlineKeyboardButton(text="Модуль 8: ИИ как усилитель призвания", url=NOTION_MODULE8)],
            [InlineKeyboardButton(text="Модуль 9: Стратегия и первые клиенты", url=NOTION_MODULE9)],
            [InlineKeyboardButton(text="Модуль 10: Система роста и масштаб", url=NOTION_MODULE10)],
            [InlineKeyboardButton(text="Закрытое комьюнити", url=COMMUNITY_LINK)]
        ])
