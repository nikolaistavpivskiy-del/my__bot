import os
import google.generativeai as genai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с Gemini. Напиши что‑нибудь!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        ai_response = response.text
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Ошибка Gemini: {e}")
        await update.message.reply_text("Что‑то пошло не так. Попробуйте ещё раз.")

def main():
    token = os.environ.get("TG_TOKEN_GEMINI")
    if not token:
        raise ValueError("❌ TG_TOKEN_GEMINI не найден!")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот с Gemini запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
