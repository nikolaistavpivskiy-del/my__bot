import telebot
from openai import OpenAI

# Настройки
TG_TOKEN = 'ТВОЙ_ТОКЕН_ТЕЛЕГРАМ'
DEEPSEEK_KEY = 'ТВОЙ_КЛЮЧ_DEEPSEEK'

importos TG_TOKEN=os.enviviron.get('TG_TOKEN')bot=telebot.Telebot(TG_TOKEN)


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
