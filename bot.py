"""
Telegram бот "Призвание"
ИСПРАВЛЕННАЯ ВЕРСИЯ - все баги устранены
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN, YOKASSA_TOKEN, COURSE_PRICE, DIAGNOSTIC_PRICE, ADMIN_ID
from database import Database
from keyboards import (
    get_start_keyboard,
    get_module1_keyboard,
    get_buy_keyboard,
    get_modules_keyboard,
    get_back_to_start_keyboard
)
from texts import TEXTS, DIAGNOSTIC_QUESTIONS
from triggers import start_triggers, stop_triggers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()


# ============ FSM СОСТОЯНИЯ ============

class OrderStates(StatesGroup):
    waiting_email = State()


class DiagnosticStates(StatesGroup):
    waiting_email = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()


DIAGNOSTIC_QUESTION_STATES = [
    DiagnosticStates.q1, DiagnosticStates.q2, DiagnosticStates.q3,
    DiagnosticStates.q4, DiagnosticStates.q5, DiagnosticStates.q6,
    DiagnosticStates.q7, DiagnosticStates.q8, DiagnosticStates.q9,
    DiagnosticStates.q10, DiagnosticStates.q11, DiagnosticStates.q12,
]


# ============ КОМАНДЫ ============

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start - проверяет статус пользователя"""
    user_id = message.from_user.id
    username = message.from_user.username or "неизвестен"

    db.add_user(user_id, username)

    if db.has_paid(user_id):
        await message.answer(
            TEXTS["welcome_back"],
            reply_markup=get_modules_keyboard(paid=True)
        )
        return

    if db.has_tag(user_id, "received_module1"):
        await message.answer(
            TEXTS["welcome_returning"],
            reply_markup=get_module1_keyboard()
        )
        return

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
        await message.answer(TEXTS["modules_paid"], reply_markup=get_modules_keyboard(paid=True))
    else:
        await message.answer(TEXTS["modules_unpaid"], reply_markup=get_modules_keyboard(paid=False))


@dp.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(TEXTS["about"])


@dp.message(Command("support"))
async def cmd_support(message: Message):
    await message.answer(TEXTS["support"])


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """Команда /stats - статистика (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        return

    stats = db.get_stats()

    conversion = 0
    if stats['got_module'] > 0:
        conversion = round(stats['paid'] / stats['got_module'] * 100, 1)

    text = f"""📊 Статистика

Всего пользователей: {stats['total']}
Получили модуль 0: {stats['got_module']}
Оплатили курс: {stats['paid']}
Конверсия модуль→оплата: {conversion}%

"""

    if stats['paid_users']:
        text += "💰 Кто купил:\n"
        for username, email, date in stats['paid_users']:
            name = f"@{username}" if username else "без username"
            mail = email if email else "email не указан"
            day = date[:10] if date else "?"
            text += f"- {name} | {mail} | {day}\n"
    else:
        text += "Покупок пока нет."

    await message.answer(text)


# ============ КНОПКИ ============

@dp.callback_query(F.data == "get_module1")
async def get_module1(callback: CallbackQuery):
    """Выдача Модуля 0 (лид-магнит)"""
    user_id = callback.from_user.id

    db.add_tag(user_id, "received_module1")

    await callback.message.answer(
        TEXTS["module1_delivery"],
        reply_markup=get_module1_keyboard()
    )

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


@dp.callback_query(F.data == "show_modules")
async def show_modules(callback: CallbackQuery):
    """Показать список модулей (из триггеров)"""
    user_id = callback.from_user.id
    has_paid = db.has_paid(user_id)

    await callback.message.answer(
        TEXTS["modules_paid"] if has_paid else TEXTS["modules_unpaid"],
        reply_markup=get_modules_keyboard(paid=has_paid)
    )
    await callback.answer()


@dp.callback_query(F.data == "buy_course")
async def buy_course(callback: CallbackQuery, state: FSMContext):
    """Покупка курса - запрашиваем email через FSM"""
    user_id = callback.from_user.id

    if db.has_paid(user_id):
        await callback.message.answer(
            "Курс уже куплен - смотри /modules",
            reply_markup=get_modules_keyboard(paid=True)
        )
        await callback.answer()
        return

    await callback.message.answer(
        TEXTS["ask_email"],
        reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(OrderStates.waiting_email)
    await callback.answer()


@dp.callback_query(F.data == "buy_diagnostic")
async def buy_diagnostic(callback: CallbackQuery, state: FSMContext):
    """Покупка диагностики - запрашиваем email через FSM"""
    user_id = callback.from_user.id

    if db.has_tag(user_id, "diagnostic_paid"):
        await callback.message.answer(
            "Диагностика уже оплачена. Ожидай разбора в течение 24 часов."
        )
        await callback.answer()
        return

    await callback.message.answer(
        TEXTS["ask_email_diagnostic"],
        reply_markup=get_back_to_start_keyboard()
    )
    await state.set_state(DiagnosticStates.waiting_email)
    await callback.answer()


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    """Вернуться на главный экран"""
    await state.clear()
    await callback.message.answer(
        TEXTS["welcome"],
        reply_markup=get_start_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "locked")
async def locked_module(callback: CallbackQuery):
    """Закрытый модуль"""
    await callback.answer(
        "Этот модуль доступен после покупки курса",
        show_alert=True
    )


# ============ EMAIL ЧЕРЕЗ FSM ============

@dp.message(OrderStates.waiting_email)
async def receive_email(message: Message, state: FSMContext):
    """Получение email для покупки курса"""
    user_id = message.from_user.id
    email = message.text.strip()

    if "@" not in email or "." not in email:
        await message.answer(
            "Неправильный формат email. Попробуй ещё раз:",
            reply_markup=get_back_to_start_keyboard()
        )
        return

    db.save_email(user_id, email)
    await state.clear()
    await send_invoice(message, user_id)


@dp.message(DiagnosticStates.waiting_email)
async def receive_diagnostic_email(message: Message, state: FSMContext):
    """Получение email для покупки диагностики"""
    user_id = message.from_user.id
    email = message.text.strip()

    if "@" not in email or "." not in email:
        await message.answer(
            "Неправильный формат email. Попробуй ещё раз:",
            reply_markup=get_back_to_start_keyboard()
        )
        return

    db.save_email(user_id, email)
    await state.clear()
    await send_diagnostic_invoice(message, user_id)


# ============ ДИАГНОСТИКА — ВОПРОСЫ ============

@dp.message(StateFilter(
    DiagnosticStates.q1, DiagnosticStates.q2, DiagnosticStates.q3,
    DiagnosticStates.q4, DiagnosticStates.q5, DiagnosticStates.q6,
    DiagnosticStates.q7, DiagnosticStates.q8, DiagnosticStates.q9,
    DiagnosticStates.q10, DiagnosticStates.q11, DiagnosticStates.q12,
))
async def handle_diagnostic_answer(message: Message, state: FSMContext):
    """Универсальный обработчик ответов на 12 вопросов диагностики"""
    data = await state.get_data()
    idx = data.get("q_index", 0)
    answers = data.get("answers", [])
    answers.append(message.text)

    if idx < 11:
        next_idx = idx + 1
        await state.set_state(DIAGNOSTIC_QUESTION_STATES[next_idx])
        await state.update_data(answers=answers, q_index=next_idx)
        await message.answer(
            f"*Вопрос {next_idx + 1} из 12*\n\n{DIAGNOSTIC_QUESTIONS[next_idx]}"
        )
    else:
        await state.clear()
        await message.answer(TEXTS["diagnostic_complete"])

        user = message.from_user
        username = f"@{user.username}" if user.username else f"id:{user.id}"
        name = user.full_name or username

        admin_text = f"📋 *Диагностика завершена*\n{name} | {username}\n\n"
        for i, (q, a) in enumerate(zip(DIAGNOSTIC_QUESTIONS, answers), 1):
            admin_text += f"*{i}.* {q}\n_{a}_\n\n"

        await bot.send_message(ADMIN_ID, admin_text)


# ФИКС: этот хендлер не перехватывает FSM-состояния
@dp.message(F.text)
async def handle_text(message: Message):
    """Обработка обычных текстовых сообщений"""
    await message.answer(
        TEXTS["unknown_message"],
        reply_markup=get_start_keyboard()
    )


# ============ ОПЛАТА ============

async def send_invoice(message: Message, user_id: int):
    """Отправка счёта за курс"""
    await message.answer_invoice(
        title="Курс 'Призвание'",
        description="Система поиска призвания за 30 дней. 10 модулей + рабочая тетрадь.",
        payload=f"course_{user_id}",
        provider_token=YOKASSA_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label="Курс 'Призвание'", amount=COURSE_PRICE * 100)
        ],
        start_parameter="buy_course",
    )


async def send_diagnostic_invoice(message: Message, user_id: int):
    """Отправка счёта за диагностику"""
    await message.answer_invoice(
        title="Персональная диагностика",
        description="12 вопросов → персональный разбор твоей ситуации за 24 часа",
        payload=f"diagnostic_{user_id}",
        provider_token=YOKASSA_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label="Персональная диагностика", amount=DIAGNOSTIC_PRICE * 100)
        ],
        start_parameter="buy_diagnostic",
    )


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    """Успешная оплата — маршрутизация по payload"""
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload

    if payload.startswith("diagnostic_"):
        db.add_tag(user_id, "diagnostic_paid")

        username = f"@{message.from_user.username}" if message.from_user.username else f"id:{user_id}"
        await bot.send_message(
            ADMIN_ID,
            f"💰 *Новая оплата диагностики!*\n{username} | 1 490 ₽"
        )

        await message.answer(TEXTS["diagnostic_confirmed"])
        await state.set_state(DiagnosticStates.q1)
        await state.update_data(answers=[], q_index=0)
        await message.answer(f"*Вопрос 1 из 12*\n\n{DIAGNOSTIC_QUESTIONS[0]}")

        logger.info(f"Оплата диагностики: {user_id}")

    else:
        db.add_tag(user_id, "paid")
        stop_triggers(user_id)

        await message.answer(
            TEXTS["after_payment"],
            reply_markup=get_modules_keyboard(paid=True)
        )

        logger.info(f"Оплата курса: {user_id}")


# ============ ЗАПУСК ============

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    db.init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
