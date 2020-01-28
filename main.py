from telebot import TeleBot
from config import TOKEN
from words import GREETINGS, NEWS_TEXT
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from keyboards import START_KB, NEWS_KB

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_bot(message):
    # message.text - Текст повідомлення
    # message.chat.id - Айди чата = фйди юзера
    # message.from_user.id - айди чата
    # message.message_id - айди сообщения

    print(message)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = [KeyboardButton(value) for value in START_KB.values()]
    kb.add(*buttons)

    bot.send_message(message.chat.id, "Hello", reply_markup=kb)


def check_greetings(message):
    return message.text.lower() in GREETINGS.keys()


@bot.message_handler(func=check_greetings)
def hello(message):
    bot.send_message(message.chat.id, GREETINGS[message.text.lower()])


@bot.message_handler(func=lambda message: message.text == START_KB["main"])
def main(message):
    bot.send_message(message.chat.id, f"{GREETINGS['здравствуй']} Ти на головній сторінці!")


@bot.message_handler(func=lambda message: message.text == START_KB["news"])
def get_news(message):
    kb = InlineKeyboardMarkup(row_width=1)

    buttons = [InlineKeyboardButton(callback_data=key, text=value) for key, value in NEWS_KB.items()]

    kb.add(*buttons)
    bot.send_message(message.chat.id, "Виберіть новину", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, NEWS_TEXT[call.data])


@bot.message_handler(content_types=["text"])
def reverse_message(message):
    text = message.text[::-1]
    bot.send_message(message.chat.id, text)


if __name__ == "__main__":
    bot.polling()