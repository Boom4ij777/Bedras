import random
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔐 Вставляем токен напрямую
BOT_TOKEN = "8064402986:AAF8Wh9hpykcJYawFmpocZAANBBEMNy47P4"

# 🎲 Ответы бота на "привет"
REPLIES = [
    "Привет, как дела?",
    "Здорова!",
    "Рад тебя видеть!",
    "Йо, ты кто?",
    "Как жизнь, брат?",
]

# 📩 Обработка сообщений
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and "привет" in update.message.text.lower():
        await update.message.reply_text(random.choice(REPLIES))

# 🚀 Запуск бота
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())