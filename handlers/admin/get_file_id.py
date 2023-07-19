from aiogram import types

from loader import dp
from filters.admin import AdminOnly


@dp.message_handler(AdminOnly(), content_types=types.ContentType.DOCUMENT)
async def get_document_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        document_id = message.document.file_id
        await message.reply(text=f'Вот id этого документа:\n{document_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        photo_id = message.photo[-1].file_id
        await message.reply(text=f'ID фотографии: \n{photo_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        video_id = message.video.file_id
        await message.reply(text=f'ID фотографии: \n{video_id}')





