"""
Telegram бот "Призвание"
Продажа курса по поиску призвания за 9,900₽
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, YOKASSA_TOKEN, COURSE_PRICE
from database import Database
from keyboards import get_start_keyboard, get_module1_keyboard, get_buy_keyboard, get_modules_keyboard
from texts import TEXTS
from triggers import start_triggers, stop_triggers

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()


# ============ КОМАНДЫ ============

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start - приветствие"""
    user_id = message.from_user.id
    username = message.from_user.username or "неизвестен"
    
    # Сохраняем пользователя в БД
    db.add_user(user_id, username)
    
    await message.answer(
        TEXTS["welcome"],
        reply_markup=get_start_keyboard()
    )


@dp.message(Command("modules"))
async def cmd_modules(message: Message):
    """Команда /modules - список модулей"""
    user_id = message.from_user.id
    has_paid = db.has_paid(user_id)
    
    if has_paid:
        text = TEXTS["modules_paid"]
        keyboard = get_modules_keyboard(paid=True)
    else:
        text = TEXTS["modules_unpaid"]
        keyboard = get_modules_keyboard(paid=False)
    
    await message.answer(text, reply_markup=keyboard)


@dp.message(Command("about"))
async def cmd_about(message: Message):
    """Команда /about - о системе"""
    await message.answer(TEXTS["about"])


@dp.message(Command("support"))
async def cmd_support(message: Message):
    """Команда /support - поддержка"""
    await message.answer(TEXTS["support"])


# ============ КНОПКИ ============

@dp.callback_query(F.data == "get_module1")
async def get_module1(callback: CallbackQuery):
    """Выдача Модуля 1"""
    user_id = callback.from_user.id
    
    # Добавляем тег "получил_модуль_1"
    db.add_tag(user_id, "received_module1")
    
    # Отправляем модуль
    await callback.message.answer(
        TEXTS["module1_delivery"],
        reply_markup=get_module1_keyboard()
    )
    
    # Запускаем триггеры (добивки)
    asyncio.create_task(start_triggers(bot, user_id, db))
    
    await callback.answer()


@dp.callback_query(F.data == "what_is_this")
async def what_is_this(callback: CallbackQuery):
    """Что это такое?"""
    await callback.message.answer(
        TEXTS["what_is_this"],
        reply_markup=get_buy_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "buy_course")
async def buy_course(callback: CallbackQuery):
    """Покупка курса"""
    user_id = callback.from_user.id
    
    # Проверяем, не купил ли уже
    if db.has_paid(user_id):
        await callback.message.answer("✅ Ты уже купил курс! Смотри /modules")
        await callback.answer()
        return
    
    # Сначала запрашиваем email
    await callback.message.answer(TEXTS["ask_email"])
    # Переводим в состояние ожидания email
    db.set_waiting_email(user_id)
    
    await callback.answer()


# ============ ПОЛУЧЕНИЕ EMAIL ============

@dp.message(F.text)
async def receive_email(message: Message):
    """Получение email от пользователя"""
    user_id = message.from_user.id
    
    # Проверяем, ждём ли email
    if not db.is_waiting_email(user_id):
        return
    
    email = message.text.strip()
    
    # Простая валидация email
    if "@" not in email or "." not in email:
        await message.answer("❌ Неправильный формат email. Попробуй ещё раз:")
        return
    
    # Сохраняем email
    db.save_email(user_id, email)
    db.clear_waiting_email(user_id)
    
    # Отправляем счёт на оплату
    await send_invoice(message, user_id)


async def send_invoice(message: Message, user_id: int):
    """Отправка счёта на оплату"""
    await message.answer_invoice(
        title="Курс 'Призвание'",
        description="Система поиска призвания за 30 дней. 10 модулей + рабочая тетрадь + комьюнити.",
        payload=f"course_{user_id}",
        provider_token=YOKASSA_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label="Курс 'Призвание'", amount=COURSE_PRICE * 100)  # в копейках
        ],
        start_parameter="buy_course",
        reply_markup=None
    )


# ============ ОПЛАТА ============

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Pre-checkout - подтверждение оплаты"""
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    """Успешная оплата"""
    user_id = message.from_user.id
    
    # Добавляем тег "оплатил"
    db.add_tag(user_id, "paid")
    
    # Останавливаем триггеры
    stop_triggers(user_id)
    
    # Отправляем поздравление
    await message.answer(
        TEXTS["after_payment"],
        reply_markup=get_modules_keyboard(paid=True)
    )
    
    logger.info(f"Успешная оплата от пользователя {user_id}")


# ============ ЗАПУСК БОТА ============

async def main():
    """Запуск бота"""
    logger.info("Бот запущен!")
    
    # Инициализация БД
    db.init_db()
    
    # Запуск polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
