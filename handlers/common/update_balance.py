from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from keyboards.inline.balance import balance_callback, coins_sum_callback
from keyboards.inline.balance import coins_sum_markup
from payments.payments import get_payment_link
from models import BotUsersModel, TransactionsModel
from states.common.update_balance import UpdateBalanceStates


@dp.callback_query_handler(balance_callback.filter(option="update_balance"))
async def update_balance(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer(
        text="Введите сумму в строке ввода или выберите один из вариантов",
        reply_markup=coins_sum_markup()
    )
    await UpdateBalanceStates.get_payment.set()


@dp.callback_query_handler(coins_sum_callback.filter(), state=UpdateBalanceStates.get_payment)
async def get_coins(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    coins = int(callback_data.get("coins"))
    amount_rub = int(callback_data.get("amount_rub"))
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    transaction = await TransactionsModel.create(bot_user, amount_rub)
    payment_link = get_payment_link(
        amount_rub=amount_rub,
        description=f"Оплата {amount_rub}р для пополнения счета на {coins} монет",
        user_id=bot_user.pk,
        invoice_id=transaction.pk,
        json_data={
            "order_id": -1,
            "has_order": False,
            "coins": coins,
            "with_bonus": True,
            "distance": 0
        }
    )
    if payment_link:
        await callback.message.answer(
            text=f"ID транзакции: {transaction.pk}\nСсылка на оплату: {payment_link}"
        )
    else:
        await callback.message.answer(
            text="При создании ссылки на оплату произошла ошибка"
        )


@dp.message_handler(state=UpdateBalanceStates.get_payment)
async def get_amount_by_message(message: types.Message, state: FSMContext):
    amount_rub = message.text
    try:
        amount_rub = int(amount_rub)
        if amount_rub > 0:
            bot_user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
            transaction = await TransactionsModel.create(bot_user, amount_rub)
            payment_link = get_payment_link(
                amount_rub=amount_rub,
                description=f"Оплата {amount_rub}р для пополнения счета на {amount_rub} монет",
                user_id=bot_user.pk,
                invoice_id=transaction.pk,
                json_data={
                    "order_id": -1,
                    "has_order": False,
                    "coins": amount_rub,
                    "with_bonus": False,
                    "distance": 0
                }
            )
        else:
            await message.answer("Значение должно быть больше 0")
    except:
        await message.answer("Значение должно быть указано целым числом")
