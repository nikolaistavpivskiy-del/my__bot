import os
import logging
from telebot import TeleBot
from langdetect import detect
from google.generativeai import GenerativeModel

# ----------------------------------------
# 🔐 Загружаем токены из Render
# ----------------------------------------
TG_TOKEN = os.getenv("TG_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

model = GenerativeModel("gemini-pro")
bot = TeleBot(TG_TOKEN)

# ----------------------------------------
# 🧠 Память диалогов (очень простая)
# ----------------------------------------
memory = {}

def add_to_memory(user_id, who, text):
    if user_id not in memory:
        memory[user_id] = []
    memory[user_id].append(f"{who}: {text}")

def build_context(user_id):
    if user_id not in memory:
        return ""
    return "\n".join(memory[user_id][-10:])  # последние 10 сообщений

# ----------------------------------------
# 🤖 Обработчик всех текстовых сообщений
# ----------------------------------------
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Антиспам
    if not text:
        return bot.reply_to(message, "Пустое сообщение? 😊 Попробуй ещё раз.")

    # Память
    add_to_memory(user_id, "Человек", text)

    # Определяем язык
    try:
        lang = detect(text)
    except:
        lang = "ru"

    context = build_context(user_id)
    prompt = f"{context}\nЧеловек: {text}\nИИ:"

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        add_to_memory(user_id, "ИИ", answer)
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, "Ой! 😟 Что-то пошло не так. Попробуй позже.")
        print("Ошибка Gemini:", e)

# ----------------------------------------
# 🚀 Запуск
# ----------------------------------------
if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling(skip_pending=True)
