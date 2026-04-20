import os
import google.generativeai as genai
import logging
from telegram import Update, ReplyKeyboardMarkup # Добавили ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL", "gemini-pro"))

# Создаем меню с кнопками
def get_main_menu():
    keyboard = [
        ['🚀 О проекте', '💡 Идеи'],
        ['❓ Помощь']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Привет! Я твой AI-помощник на базе Gemini.*\n\n"
        "Пиши любой вопрос в чат или воспользуйся кнопками меню ниже 👇"
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=get_main_menu(), 
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Логика обработки кнопок
    if user_text == '🚀 О проекте':
        response_text = "Я — бот, созданный для демонстрации возможностей нейросетей в Telegram. Мой мозг — это Gemini!"
    elif user_text == '💡 Идеи':
        response_text = "Предложи мне тему, и я набросаю список идей! Например: 'Идеи для домашнего проекта'."
    elif user_text == '❓ Помощь':
        response_text = "Просто отправь мне текстовое сообщение, и я отвечу на него. Если я зависну, нажми /start."
    else:
        # Если это не кнопка, отправляем запрос в Gemini
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        try:
            response = await model.generate_content_async(user_text)
            response_text = response.text
        except Exception as e:
            logger.error(f"Ошибка Gemini: {e}")
            response_text = "Произошла ошибка при обращении к ИИ. Попробуй позже."

    # Отправляем ответ (проверяем длину на всякий случай)
    if len(response_text) > 4000:
        response_text = response_text[:4000] + "..."
        
    await update.message.reply_text(response_text)

def main():
    token = os.environ.get("TG_TOKEN_GEMINI")
    if not token:
        raise ValueError("TG_TOKEN_GEMINI не найден!")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот с кнопками запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
