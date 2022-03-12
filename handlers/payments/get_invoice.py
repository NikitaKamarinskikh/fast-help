import json
from aiogram import types
from loader import dp, bot
from data.config import REFERRER_BONUS_PERCENT, OrderStatuses
from models import BotUsersModel, TransactionsModel, OrdersModel
from notifications.notifications import notify_referrer, notify_user_about_success_transaction


def count_bonus(sum_: float):
    if sum_ == 50:
        return 3
    return round(REFERRER_BONUS_PERCENT * (1 / 100) * sum_)


async def set_order_waiting_for_start_status(order_id: int):
    order = await OrdersModel.get_by_id(order_id)
    order.status = OrderStatuses.waiting_for_start
    order.save()


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def process_success_payment(message: types.Message):
    """
    payload example
    {'order_id': 144258, 'has_order': True, 'coins': 30, 'with_bonus': False,
    'distance': 500, 'transaction_id': 33}
    """
    amount = message.successful_payment.total_amount

    data = json.loads(message.successful_payment.invoice_payload.replace("'", '"'))

    user_id = message.from_user.id
    transaction_id = data.get("transaction_id")
    order_id = int(data.get("order_id"))
    has_order = data.get("has_order")
    coins = int(data.get("coins"))
    distance = int(data.get("distance"))
    with_bonus = data.get("with_bonus")

    print(user_id, transaction_id, amount, order_id, has_order, coins, distance, with_bonus)

    user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    transaction = await TransactionsModel.get_by_id(transaction_id)
    reply_markup = None
    new_user_coins = user.coins
    if not transaction.is_paid:
        transaction.is_paid = True
        transaction.save()
        if has_order:
            if with_bonus:
                if distance == 500:
                    coins -= 30
                if distance == 1000:
                    coins -= 50
                current_user_coins = user.coins
                new_user_coins = current_user_coins + coins
                user.coins = new_user_coins
                user.save()
            # reply_markup = send_order_to_workers_markup(order_id, distance)
            await set_order_waiting_for_start_status(order_id)
        else:
            current_user_coins = user.coins
            new_user_coins = current_user_coins + coins
            user.coins = new_user_coins
            user.save()

        await notify_user_about_success_transaction(user.telegram_id, new_user_coins, reply_markup)

        if user.referrer:
            bonus = count_bonus(amount)
            referrer = await BotUsersModel.get_by_id(user.referrer.pk)
            new_referrer_balance = referrer.coins + bonus
            referrer.coins = new_referrer_balance
            referrer.save()
            await notify_referrer(referrer.telegram_id, bonus, new_referrer_balance)

    await message.answer(
        text="Оплата прошла"
    )




