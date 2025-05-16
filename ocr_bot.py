from aiogram import Bot, Dispatcher, types
import pytesseract
from PIL import Image
import io
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_photo(message: types.Message):
    if not message.photo:
        return

    await message.answer("📷 Получил фото. Начинаю распознавание...")

    # Скачиваем фото во временное хранилище в памяти
    photo = message.photo[-1]
    photo_file = io.BytesIO()
    await bot.download(photo, destination=photo_file)
    photo_file.seek(0)

    # Открываем и распознаём
    image = Image.open(photo_file)
    text = pytesseract.image_to_string(image, lang='rus')

    if text.strip():
        await message.answer(f"✅ Вот, что удалось распознать:\n\n{text}")
    else:
        await message.answer("❗ Не удалось распознать текст. Попробуйте другое фото.")

async def main():
    dp.message.register(handle_photo)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
