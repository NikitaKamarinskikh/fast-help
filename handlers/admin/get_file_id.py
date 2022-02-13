from aiogram import types
from loader import dp
from filters.admin import AdminOnly


@dp.message_handler(AdminOnly(), content_types=types.ContentType.DOCUMENT)
async def get_document_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        document_id = message.document.file_id
        await message.reply(text=f'Вот id этого документа:\n{document_id}')





