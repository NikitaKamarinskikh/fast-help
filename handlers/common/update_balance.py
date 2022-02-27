from loader import dp
from aiogram import types
from keyboards.inline.balance import balance_callback, coins_sum_callback
from keyboards.inline.balance import coins_sum_markup
from payments.payments import get_payment_link
from models import BotUsersModel


@dp.callback_query_handler(balance_callback.filter(option="update_balance"))
async def update_balance(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer(
        text="Введите сумму в строке ввода или выберите один из вариантов",
        reply_markup=coins_sum_markup()
    )


@dp.callback_query_handler(coins_sum_callback.filter())
async def get_coins(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    coins = int(callback_data.get("coins"))
    amount_rub = int(callback_data.get("amount_rub"))
    # payment_link = get_payment_link(amount_rub, "Тестовый запрос")
    payment_link = "test"
    if payment_link:
        await callback.message.answer(
            text=f"Ссылка на оплату: {payment_link}"
        )
    else:
        await callback.message.answer(
            text="При создании ссылки на оплату произошла ошибка"
        )

    # Все что написано дальше нужно вынести в отдельный обработчик
    bot_user = await BotUsersModel.add_coins(callback.from_user.id, coins)
    await callback.message.answer(
        text=f"Оплата прошла успешно, ваш баланс: {bot_user.coins} монет"
    )



