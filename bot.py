import telebot
import os
import google.generativeai as genai

# 1. Токены (Render автоматически подставит переменные окружения)
TG_TOKEN = os.getenv('TG_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# Проверка токенов
if not TG_TOKEN:
    raise ValueError("Ошибка: TG_TOKEN не найден в переменных окружения!")

if not GEMINI_KEY:
    raise ValueError("Ошибка: GEMINI_KEY не найден в переменных окружения!")

# 2. Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # лёгкая и быстрая модель

# 3. Настройка Telegram-бота
bot = telebot.TeleBot(TG_TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Привет! 😊 Я бот на Google Gemini. Спроси что угодно — и я отвечу!"
    )

# Обработка всех текстовых сообщений
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    text = message.text.strip()

    try:
        response = model.generate_content(text)  # обращение к ИИ
        answer = response.text.strip()

        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, "Ой! 😅 Что-то пошло не так. Попробуй ещё раз.")
        print("Ошибка Gemini:", e)

# Запуск бесконечного поллинга
bot.infinity_polling(skip_pending=True)
