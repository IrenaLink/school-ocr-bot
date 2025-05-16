import io
import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализируем OCR (русский + английский)
ocr = PaddleOCR(use_angle_cls=True, lang='ru')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_photo(message: types.Message):
    if not message.photo:
        return

    await message.answer("📷 Получил фото. Начинаю нейросетевое распознавание...")
    photo = message.photo[-1]
    photo_file = io.BytesIO()
    await bot.download(photo, destination=photo_file)
    photo_file.seek(0)

    # Всё дальше — строго внутри этой функции, с отступом!
    image = Image.open(photo_file).convert('RGB')
    image_np = np.array(image)

    result = ocr.ocr(image_np, cls=True)

    text_result = ''
    for line in result[0]:
        text_result += line[1][0] + '\n'

    if text_result.strip():
        await message.answer(f"✅ Вот, что удалось распознать:\n\n{text_result}")
    else:
        await message.answer("❗ Не удалось распознать текст. Попробуйте другое фото.")

async def main():
    dp.message.register(handle_photo)
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 Бот успешно запущен и использует PaddleOCR. Жду фото...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
