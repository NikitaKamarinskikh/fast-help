from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram import types
from keyboards.inline.balance import balance_callback, coins_sum_callback
from keyboards.inline.balance import coins_sum_markup
from keyboards.inline.yes_or_no import yes_or_no_callback
from payments.payments import get_payment_link, send_invoice
from models import BotUsersModel, TransactionsModel
from states.common.update_balance import UpdateBalanceStates
from states.workers.chose_order import ChoseOrderStates


@dp.callback_query_handler(yes_or_no_callback.filter(question="update_balance", choice="yes"),
                           state=ChoseOrderStates.chose_order)
async def update_balance_by_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    await callback.answer()
    await callback.message.answer(
        text="Введите сумму в строке ввода или выберите один из вариантов",
        reply_markup=coins_sum_markup()
    )
    await UpdateBalanceStates.get_payment.set()


@dp.callback_query_handler(balance_callback.filter(option="update_balance"))
async def update_balance(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer(
        text="Введите сумму в строке ввода или выберите один из вариантов",
        reply_markup=coins_sum_markup()
    )
    await UpdateBalanceStates.get_payment.set()


@dp.callback_query_handler(coins_sum_callback.filter(), state=UpdateBalanceStates.get_payment)
async def get_coins(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    coins = int(callback_data.get("coins"))
    amount_rub = int(callback_data.get("amount_rub"))
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    transaction = await TransactionsModel.create(bot_user, amount_rub)
    description = f"Оплата {amount_rub}р для пополнения счета на {coins} монет"
    payload = {
        "order_id": -1,
        "has_order": 0,
        "coins": coins,
        "with_bonus": 0,
        "distance": 0,
        "transaction_id": transaction.pk
    }
    await state.finish()
    try:
        await send_invoice(callback.from_user.id, f"Пополнение баланса", description, str(payload), amount_rub)
    except:
        await callback.message.answer("При создании платежа произошла ошибка. Повторите попытку позже")


@dp.message_handler(state=UpdateBalanceStates.get_payment)
async def get_amount_by_message(message: types.Message, state: FSMContext):
    amount_rub = message.text
    try:
        amount_rub = int(amount_rub)
        if amount_rub > 0:
            bot_user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
            transaction = await TransactionsModel.create(bot_user, amount_rub)
            coins = amount_rub
            description = f"Оплата {amount_rub}р для пополнения счета на {coins} монет"
            payload = {
                "order_id": -1,
                "has_order": 0,
                "coins": coins,
                "with_bonus": 0,
                "distance": 0,
                "transaction_id": transaction.pk
            }
            await state.finish()
            try:
                await send_invoice(message.from_user.id, f"Пополнение баланса", description, str(payload), amount_rub)
            except:
                await message.answer("При создании платежа произошла ошибка. Повторите попытку позже")
        else:
            await message.answer("Значение должно быть больше 0")
    except:
        await message.answer("Значение должно быть указано целым числом")
