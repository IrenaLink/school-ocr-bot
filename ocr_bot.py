from aiogram import Bot, Dispatcher, types, executor
import pytesseract
from PIL import Image
import io

# Твой токен от BotFather сюда
import os

API_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Путь к установленному Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик фото
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.reply("📷 Получил фото. Начинаю распознавание...")

    # Скачиваем фото во временное хранилище в памяти
    photo = await message.photo[-1].download(destination_file=io.BytesIO())
    photo.file.seek(0)

    # Открываем фото и передаём в OCR
    image = Image.open(photo.file)
    text = pytesseract.image_to_string(image, lang='rus')

    # Отправляем результат
    if text.strip():
        await message.reply(f"✅ Вот, что удалось распознать:\n\n{text}")
    else:
        await message.reply("❗ Не удалось распознать текст. Попробуйте фото получше.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
