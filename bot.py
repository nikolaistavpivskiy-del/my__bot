import os
import logging
from threading import Thread
from flask import Flask  # Не забудь добавить в requirements.txt
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Настройка веб-сервера для Render (чтобы сервис не засыпал)
server = Flask('')

@server.route('/')
def home():
    return "Бот активен!"

def run_web():
    # Render автоматически назначает порт через переменную PORT
    port = int(os.environ.get("PORT", 10000))
    server.run(host='0.0.0.0', port=port)

# 2. Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3. Инициализация Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL",("models/gemini-1.5-flash"))

def get_main_menu():_
keyboard = [['🚀 О проекте', '💡 Идеи'], ['❓ Помощь']]
return ReplyKeyboardMarkup(keyboard,resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот на базе Gemini. Чем могу помочь?",
        reply_markup=get_main_menu()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == '🚀 О проекте':
        response_text = "Я — умный бот на базе Gemini AI, запущенный на Render!"
    elif user_text == '💡 Идеи':
        response_text = "Напиши тему, и я помогу придумать что-то крутое."
    elif user_text == '❓ Помощь':
        response_text = "Просто присылай текст, и я отвечу."
    else:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        try:
            response = await model.generate_content_async(user_text)
            response_text = response.text
        except Exception as e:
            logger.error(f"Ошибка Gemini: {e}")
            response_text = "Ошибка связи с ИИ. Попробуй позже."

    await update.message.reply_text(response_text)

def main():
    # ЗАПУСК ВЕБ-СЕРВЕРА в фоновом потоке
    Thread(target=run_web).start()

    token = os.environ.get("TG_TOKEN_GEMINI")
    if not token:
        raise ValueError("TG_TOKEN_GEMINI не найден!")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот и веб-сервер запущены...")
    app.run_polling()

if __name__ == "__main__":
    main()

