import json
from aiogram import types

from common import get_candidates_by_filters
from keyboards.default.main import main_markup
from loader import dp, bot
from data.config import REFERRER_BONUS_PERCENT, OrderStatuses
from models import BotUsersModel, TransactionsModel, OrdersModel, WithdrawalsModel
from notifications.notifications import notify_referrer, notify_user_about_success_transaction, \
    notify_workers_about_new_order
from data.config import distances


def count_bonus(sum_: float):
    if sum_ == 50:
        return 3
    return round(REFERRER_BONUS_PERCENT * (1 / 100) * sum_)


async def set_order_waiting_for_start_status(order_id: int):
    order = await OrdersModel.get_by_id(order_id)
    order.status = OrderStatuses.waiting_for_start
    order.save()


async def send_order_to_workers(order_id: int, user_telegram_id: int):
    order = await OrdersModel.get_by_id(order_id)
    candidates = await get_candidates_by_filters(order, user_telegram_id)
    await notify_workers_about_new_order(candidates, order)


@dp.pre_checkout_query_handler(state="*")
async def process_pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT, state="*")
async def process_success_payment(message: types.Message):
    """
    payload example
    {'order_id': 144258, 'has_order': 1, 'coins': 30, 'with_bonus': 0,
    'distance': 500, 'transaction_id': 33}
    """
    amount = message.successful_payment.total_amount
    data = json.loads(message.successful_payment.invoice_payload.replace("'", '"'))
    transaction_id = data.get("transaction_id")
    order_id = int(data.get("order_id"))
    has_order = data.get("has_order")
    coins = int(data.get("coins"))
    distance = int(data.get("distance"))
    with_bonus = data.get("with_bonus")

    user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    transaction = await TransactionsModel.get_by_id(transaction_id)
    reply_markup = None
    user_coins_before = user.coins
    if not transaction.is_paid:
        transaction.is_paid = True
        transaction.save()
        if has_order:
            await set_order_waiting_for_start_status(order_id)
            # if with_bonus:
            if distance == distances.short.meters:
                coins -= distances.short.customer_price
            if distance == distances.middle.meters:
                coins -= distances.middle.customer_price
        new_user_coins = user.coins + coins
        user = await BotUsersModel.add_coins(message.from_user.id, coins)
        order = await OrdersModel.get_by_id(order_id)
        await notify_user_about_success_transaction(user.telegram_id, new_user_coins, reply_markup)
        await WithdrawalsModel.create(order, user, user_coins_before, coins, user.coins)

        if user.referrer:
            bonus = count_bonus(amount)
            referrer = await BotUsersModel.get_by_id(user.referrer.pk)
            new_referrer_balance = referrer.coins + bonus
            referrer.coins = new_referrer_balance
            referrer.save()
            await notify_referrer(referrer.telegram_id, bonus, new_referrer_balance)

    if has_order:
        await message.answer("Ищу исполнителей...")
        await send_order_to_workers(order_id, message.from_user.id)
        await message.answer(
            text="Ваше задание отправлено исполнителям рядом",
            reply_markup=main_markup
        )



