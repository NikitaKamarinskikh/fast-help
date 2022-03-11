from aiogram import types
from loader import dp, bot


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
    print(message.successful_payment.invoice_payload)
    if message.successful_payment.invoice_payload == "test_payload":
        await message.answer("payload прошел")
    await message.answer(
        text="Оплата прошла"
    )



