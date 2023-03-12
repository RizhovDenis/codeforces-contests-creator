import click


@click.group(name='telegram-bot')
def telegram_group():
    """ Telegram service """


@telegram_group.command(name='run')
def telegram_bot():
    import telebot
    from telebot import types

    from components.problem.models import Contest
    from apps.telegram.utils.logic import show_topics, show_contest, look_for_contests, exception_message
    from settings import proj_conf

    bot = telebot.TeleBot(proj_conf.telegram_token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        topics_btn = types.KeyboardButton(
            text='Показать темы контестов'
        )
        main_message = 'Здравствуйте! Этот бот поможет вам подобрать контесты на алгоритмы и структуры данных по теме и сложности\n'

        markup.add(topics_btn)

        bot.send_message(
            message.chat.id,
            main_message,
            reply_markup=markup
        )

    @bot.message_handler()
    def text_handler(message):
        if message.text == 'Показать темы контестов':
            return show_topics(message, bot)

        contests = Contest.get_unique_topics()
        topics = [contest.topic.lower() for contest in contests]
        chars = message.text.split()
        req_topic = ' '.join(chars[0:-1])

        if len(chars) >= 2 and req_topic.lower() in topics and chars[-1].isnumeric():
            return look_for_contests(message, bot, req_topic, chars)

        if len(chars) == 2 and chars[0].lower() == 'контест' and chars[1].isnumeric():
            return show_contest(message, bot, chars)

        return exception_message(message, bot)

    bot.polling(none_stop=True)
