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
bot.infinity_polling(skip_pending
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
bot.infinity_polling(skip_pending
