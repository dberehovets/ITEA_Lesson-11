from mongoengine.errors import  ValidationError, DoesNotExist
from telebot import TeleBot
from config import TOKEN
from home.model import User

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_bot(message):
    try:
        _get_data(message)
    except DoesNotExist:
        User(telegram_id=message.from_user.id).save()
        bot.send_message(message.chat.id, "Hello! Please type your name.")


@bot.message_handler(content_types=["text"])
def get_name(message):
    user = User.objects(telegram_id=message.from_user.id).get()
    for key, value in user.get_fields().items():
        if not value:
            users = User._get_collection()
            users.find_one_and_update({"telegram_id": message.from_user.id}, {"$set": {key: message.text}})
            break
    _get_data(message)


def _get_data(message):
    user = User.objects(telegram_id=message.from_user.id).get()
    all_fields_filled = True
    for key, value in user.get_fields().items():
        if not value:
            all_fields_filled = False
            bot.send_message(message.chat.id, f"Please type your {key}")
            break
    if all_fields_filled:
        bot.send_message(message.chat.id, "Data is stored. Thank you!")


if __name__ == "__main__":
    bot.polling()