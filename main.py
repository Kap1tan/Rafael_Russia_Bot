import logging
import asyncio
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)

# Определяем состояния диалога
(
    START,
    QUESTION1,
    QUESTION2,
    QUESTION3,
    WAIT_CHECKLIST_PROMPT,
) = range(5)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo_url = "https://postimg.cc/0bv6fLWx"  # Замените на нужный URL изображения
    caption = (
        "Привет 👋, это бот помощник @Rafael_Russia и с помощью меня ты познаешь мир закупов, если еще не знаком с ним и узнаешь новые фишки, если уже закупщик с опытом\n\n"
        "Если ты не знаком со мной, то давай для начала познакомимся.\n\n"
        "Меня зовут Рафаэль, мне 19 лет, и я уже более 3 лет работаю закупщиком и являюсь самым медийным закупщиком на данный момент, отлил совместно с командой и агентством @RSMediaHolding более 70 миллионов рублей, обучил совместно с командой и выпустил на рынок более 450+ закупщиков, отзывы тут @Rafaei_Russia\n\n"
        "Ну, а теперь давай перейдем к нашему материалу, но для начала пройди тест, дабы я понимал, какой у тебя уровень знаний вниз 👇🏻"
    )
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Пройти тест", callback_data="start_test")]]
    )
    await update.message.reply_photo(photo=photo_url, caption=caption, reply_markup=keyboard)
    return START


# Обработка нажатия на кнопку "Пройти тест"
async def start_test_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    # Отправляем первый вопрос
    question_text = "Что необходимо сделать в первую очередь, когда начинаешь работать закупщиком?"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Изучить аналитику каналов", callback_data="q1_a1")],
        [InlineKeyboardButton("Оформить профиль", callback_data="q1_a2")],
        [InlineKeyboardButton("Искать клиентов", callback_data="q1_a3")],
    ])
    await query.message.reply_text(question_text, reply_markup=keyboard)
    return QUESTION1


# Обработка ответа на первый вопрос
async def handle_question1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    selected = query.data  # Ожидается: "q1_a1", "q1_a2" или "q1_a3"
    if selected == "q1_a1":
        response_text = "Правильно! Изучить аналитику каналов — это база, без нее никуда."
    else:
        response_text = "Неправильно."
    await query.message.reply_text(response_text)

    # Отправляем второй вопрос
    question_text = "Сколько в среднем зарабатывает закупщик?"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("20/30к", callback_data="q2_a1")],
        [InlineKeyboardButton("50/70к", callback_data="q2_a2")],
        [InlineKeyboardButton("150/200к", callback_data="q2_a3")],
    ])
    await query.message.reply_text(question_text, reply_markup=keyboard)
    return QUESTION2


# Обработка ответа на второй вопрос
async def handle_question2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    selected = query.data
    if selected == "q2_a3":
        response_text = (
            "Правильно, закупщик, имеющий несколько постоянных клиентов, уже может зарабатывать более 150 тысяч рублей в месяц — тому пример мои ученики."
        )
    else:
        response_text = "Неправильно."
    await query.message.reply_text(response_text)

    # Отправляем третий вопрос
    question_text = "Какие основные проблемы у закупщика?"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("заполнение таблицы", callback_data="q3_a1")],
        [InlineKeyboardButton("поиск клиентов", callback_data="q3_a2")],
        [InlineKeyboardButton("анализ каналов", callback_data="q3_a3")],
    ])
    await query.message.reply_text(question_text, reply_markup=keyboard)
    return QUESTION3


# Обработка ответа на третий вопрос
async def handle_question3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    selected = query.data
    if selected == "q3_a2":
        response_text = (
            "Верно! Большинство проблем у закупщиков — это поиск клиентов, ведь у многих нет понимания, где их искать. "
            "Некоторые сидят без клиентов, и сейчас мы это исправим с помощью чек-листа."
        )
    else:
        response_text = "Неправильно."
    await query.message.reply_text(response_text)

    # Ждем 3 секунды перед отправкой сообщения с вопросами о пользователе
    await asyncio.sleep(2)
    info_text = (
        "Прежде, чем я вышлю тебе первый урок — мне нужно узнать больше информации о тебе.\n\n"
        "Чтобы помочь человеку стартануть в закупах, я должен понимать, с чем он пришел.\n\n"
        "Отвечаю лично, полностью индивидуальный подход. Всё конфиденциально.\n\n"
        "Поэтому: очень важно, чтобы ты ответил на вопросы ниже⬇️\n\n"
        "1. Как тебя зовут? Сколько лет? В каком городе живешь?\n"
        "2. Чем занимаешься? Работаешь/учишься, расскажи подробнее\n"
        "3. Сколько зарабатываешь сейчас? Сколько хотела бы зарабатывать?\n"
        "4. Был ли опыт в том, чтобы построить свой бизнес? (Не обязательно на закупах)\n\n"
        "Ответы присылай мне в личку: @Rafael_Russia"
    )
    await query.message.reply_text(info_text)

    # Ждем 60 секунд и отправляем сообщение с кнопкой для чек-листа
    await asyncio.sleep(60)
    checklist_text = "ГОТОВО, КИДАЮ ЧЕК-ЛИСТ?"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ЧЕК-ЛИСТ", callback_data="send_checklist")]]
    )
    await query.message.reply_text(checklist_text, reply_markup=keyboard)
    return WAIT_CHECKLIST_PROMPT


# Обработка нажатия на кнопку "ЧЕК-ЛИСТ"
async def send_checklist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    # Отправляем файл чек-листа (укажите корректный путь к файлу)
    checklist_file_path = "ЧекЛист.pdf"
    with open(checklist_file_path, "rb") as file:
        await query.message.reply_document(document=file, filename="checklist.pdf")

    # Запускаем задачу по отправке отложенного сообщения через 60 секунд
    asyncio.create_task(schedule_followup(query.message.chat.id, context))
    return ConversationHandler.END


# Функция для отложенной отправки сообщения
async def schedule_followup(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(60)
    message_text = (
        "Как тебе инфа? Получил пользу? Мне очень важно понимать, на сколько качественный продукт, "
        "именно от тебя жду обратную связь в личку — @Rafael_Russia\n\n"
        "Отправь 🔥, если инфа была полезна\n\n"
        "Или 💩, если все уже знал\n\n"
        "Всем тем, кто отписал — дам в подарок 5 секретных способов поиска клиента прямо на бесплатной консультации со мной."
    )
    await context.bot.send_message(chat_id=chat_id, text=message_text)


# Обработчик команды /cancel для завершения диалога
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    TOKEN = "7714280353:AAG5KcGM-jZRJN3cMhQOmQzBgsup9XTS8zY"  # либо укажите токен напрямую
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(start_test_callback, pattern="^start_test$")],
            QUESTION1: [CallbackQueryHandler(handle_question1, pattern="^q1_")],
            QUESTION2: [CallbackQueryHandler(handle_question2, pattern="^q2_")],
            QUESTION3: [CallbackQueryHandler(handle_question3, pattern="^q3_")],
            WAIT_CHECKLIST_PROMPT: [CallbackQueryHandler(send_checklist, pattern="^send_checklist$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
