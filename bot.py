import telebot
import os
from openai import OpenAI

# Настройки (берем из Render)
TG_TOKEN = os.environ.get('TG_TOKEN')
DEEPSEEK_KEY = os.environ.get('DEEPSEEK_KEY')

bot = telebot.TeleBot(TG_TOKEN)


# Настраиваем клиент для DeepSeek
client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот на базе DeepSeek. Спрашивай что угодно!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Отправляем текст пользователя в нейросеть
        response = client.chat.completions.create(
            model="deepseek-chat", # Или deepseek-reasoner для сложных задач
            messages=[
                {"role": "system", "content": "Ты полезный ассистент."},
                {"role": "user", "content": message.text},
            ],
            stream=False
        )
        
        # Получаем ответ от ИИ
        ai_text = response.choices[0].message.content
        bot.reply_to(message, ai_text)
        
    except Exception as e:
        bot.reply_to(message, "Ой, что-то пошло не так. Попробуй позже!")
        print(f"Ошибка: {e}")

bot.infinity_polling()
