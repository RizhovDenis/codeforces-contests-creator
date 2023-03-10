from telebot import types


class ButtonsBot:
    inline_show_topics = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.InlineKeyboardButton(
            text='Показать темы контестов',
            callback_data='show topics'
        )
    )


buttons = ButtonsBot()
