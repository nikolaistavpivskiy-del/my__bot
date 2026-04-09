import telebot
import os
import google.generativeai as genai

# 1. Настройки (Render сам подставит значения)
TG_TOKEN = os.environ.get('TG_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# 2. Настройка Близнецов
genai.configure(api_key=GEMINI_KEY)
# Используем ту самую модель Flash, которую ты выбрал
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Теперь я работаю на Gemini 3. Спрашивай что угодно!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Прямой запрос ко мне
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Ой, я запнулся. Попробуй еще раз!")
        print(f"Ошибка: {e}")

bot.infinity_polling()
