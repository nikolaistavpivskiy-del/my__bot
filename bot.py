import os
import google.generativeai as genai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Gemini с использованием переменных окружения
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    # Получаем модель из переменной окружения, по умолчанию — gemini-pro
    model_name = os.environ.get("GEMINI_MODEL", "gemini-pro")
    model = genai.GenerativeModel(model_name)
    logger.info(f"Используется модель Gemini: {model_name}")
except Exception as e:
    logger.error(f"Ошибка инициализации Gemini: {e}")
    raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я бот с Gemini. Напиши что‑нибудь!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text

    try:
        # Отправляем запрос к Gemini
        response = model.generate_content(user_message)
        ai_response = response.text

        # Ограничиваем длину ответа (Telegram ограничивает 4096 символов)
        if len(ai_response) > 4000:
            ai_response = ai_response[:4000] + "\n\n(Ответ обрезан для соответствия ограничениям Telegram)"

        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Ошибка Gemini: {e}")
        await update.message.reply_text("Что‑то пошло не так. Попробуйте ещё раз.")

def main():
    """Основная функция запуска бота"""
    token = os.environ.get("TG_TOKEN_GEMINI")
    if not token:
        raise ValueError("❌ TG_TOKEN_GEMINI не найден! Проверьте переменные окружения.")

    # Создаём приложение
    app = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот с Gemini запущен...")
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
  
  
