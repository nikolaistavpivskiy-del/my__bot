import telebot
import os
import google.generativeai as genai
from langdetect import detect

# -------------------------------------------------------
# 1. Загрузка токенов из переменных окружения
# -------------------------------------------------------
TG_TOKEN = os.getenv("TG_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not TG_TOKEN:
    raise ValueError("❌ Ошибка: TG_TOKEN не найден в переменных окружения")
if not GEMINI_KEY:
    raise ValueError("❌ Ошибка: GEMINI_KEY не найден в переменных окружения")

# -------------------------------------------------------
# 2. Настройка Gemini
# -------------------------------------------------------
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------------------------------
# 3. Создание Telegram-бота
# -------------------------------------------------------
bot = telebot.TeleBot(TG_TOKEN)

# -------------------------------------------------------
# Память диалогов: user_id → список сообщений
# -------------------------------------------------------
user_memory = {}

MAX_CONTEXT = 10  # хранить последние 10 сообщений


def add_to_memory(user_id, role, text):
    """Сохраняет реплики в память (роль: 'user' или 'bot')"""
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({"role": role, "text": text})

    # Ограничиваем длину истории
    if len(user_memory[user_id]) > MAX_CONTEXT:
        user_memory[user_id] = user_memory[user_id][-MAX_CONTEXT:]


def build_context(user_id):
    """Создает строку диалога для Gemini"""
    if user_id not in user_memory:
        return ""

    dialog = ""
    for msg in user_memory[user_id]:
        prefix = "Человек:" if msg["role"] == "user" else "ИИ:"
        dialog += f"{prefix} {msg['text']}\n"

    return dialog


# -------------------------------------------------------
# Команда /start
# -------------------------------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Привет! 😊 Я ИИ-бот на Google Gemini.\n"
        "Спроси что угодно — помогу!"
    )


# -------------------------------------------------------
# Обработчик всех текстовых сообщений
# -------------------------------------------------------
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # 🛡 Антиспам — запрещаем отправлять пустые сообщения
    if not text:
        return bot.reply_to(message, "Пустое сообщение? 😅 Попробуй ещё раз.")

    # 🧠 Добавляем сообщение в память
    add_to_memory(user_id, "user", text)

    # 🈯 Определяем язык пользователя
    try:
        lang = detect(text)
    except:
        lang = "ru"

    context = build_context(user_id)
    prompt = f"{context}\nЧеловек: {text}\nИИ:"

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()

        # 🧠 Сохраняем ответ в историю
        add_to_memory(user_id, "bot", answer)

        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, "Ой! 😅 Что-то пошло не так. Попробуй ещё раз.")
        print("Ошибка Gemini:", e)


# -------------------------------------------------------
# Запуск вечного polling
# -------------------------------------------------------
bot.infinity_polling(skip_pending=True)
