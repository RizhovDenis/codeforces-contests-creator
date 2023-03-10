import click


@click.group(name='parser')
def parser_group():
    """ Parser service """


@parser_group.command(name='parse-codeforces')
def parse_codeforces_problems():
    import time
    import requests

    from datetime import datetime, timedelta
    from settings import proj_conf

    from apps.parser.utils.parser import parsing_pages

    interval = datetime.utcnow()
    time_expired = interval + timedelta(seconds=proj_conf.parsing_frequency)

    while True:
        if interval < time_expired:
            time.sleep(proj_conf.parsing_frequency // 10)
            interval = datetime.utcnow()
            continue

        req = requests.get(url=proj_conf.codeforce_url)

        while req.status_code != 200:
            req = requests.get(url=proj_conf.codeforce_url)

        parsing_pages(page=req.text)

        interval = interval + timedelta(seconds=proj_conf.parsing_frequency)
        time_expired = interval + timedelta(seconds=proj_conf.parsing_frequency)


@parser_group.command(name='telegram-bot')
def telegram_bot():
    import telebot
    from telebot import types

    from components.problem.models import Contest
    from apps.parser.utils.telegrambot import show_topics, show_contest, look_for_contests, exception_message
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
