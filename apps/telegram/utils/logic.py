from components.problem.models import Contest, Problem


def show_topics(message, bot):
    contests = Contest.get_unique_topics()
    main_message = 'Выберите тему и сложность затем отправьте название в чат\n'

    for num, contest in enumerate(contests):
        if contest.topic:
            complexities = [str(compl.complexity) for compl in Contest.get_by_topic(topic=contest.topic)]
            main_message += '\n' + \
                            f'<b style="color: #777777;">{num}</b>. {contest.topic.title()} - {", ".join(complexities)}'

    return bot.send_message(
        message.chat.id,
        text=main_message + '\n\nПример: <b>two pointers 800</b>\n',
        parse_mode='html'
    )


def show_contest(message, bot, chars):
    problems = Problem.get_by_contest_id(int(chars[1]))
    contest = Contest.get_by_id(int(chars[1]))
    mess = ''
    for problem in problems:
        mess += f'{problem.number}.  <a href="{problem.url}">{problem.name}</a> - x{problem.count_decided}\n'

    if problems and contest:
        return bot.send_message(
            message.chat.id,
            text=f'Контест №{chars[1]}. Тема - {contest[0].topic.title()}\n\n' + mess,
            parse_mode='html'
        )

    return None


def look_for_contests(message, bot, req_topic, chars):
    new_contests = Contest.get_by_topic(topic=req_topic.lower())
    complexities = [str(contest.complexity) for contest in new_contests]

    if chars[-1] not in complexities:
        return bot.send_message(
            message.chat.id,
            text='Контест c данной сложностью не найден. Посмотрите список тем и сложностей'
        )

    problems = Contest.get_by_topic_and_complexity(req_topic.lower(), int(chars[-1]))
    ids = [problem.id for problem in problems]
    mess = ''

    for i in ids:
        if ids[-1] == i:
            mess += f'№{i}'
        else:
            mess += f'№{i}, '

    example = f'\n\nПример - контест {ids[0]}'

    return bot.send_message(
        message.chat.id,
        text=f'Выберите номер контеста. Контесты на тему - {req_topic.title()} сложностью - {chars[-1]}\n\n' + \
             mess + example
    )


def exception_message(message, bot):
    from apps.telegram.utils.navigation import buttons

    markup = buttons.inline_show_topics
    return bot.send_message(
        message.chat.id,
        text='Контест на данную тему с данной сложностью не найден. Посмотрите список тем',
        reply_markup=markup
    )
