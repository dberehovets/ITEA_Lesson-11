from mongoengine.errors import  ValidationError
from telebot import TeleBot
from config import TOKEN
from home.model import User

bot = TeleBot(TOKEN)

user_fields = []
user_data = dict()


@bot.message_handler(commands=["start"])
def start_bot(message):
    global user_fields
    user_fields = User.get_fields()
    bot.send_message(message.chat.id, "Hello! Please type your name.")


@bot.message_handler(content_types=["text"])
def get_name(message):
    try:
        field = user_fields.pop(0)
        user_data[field] = message.text
        if user_fields:
            bot.send_message(message.chat.id, f"Please type your {user_fields[0]}")
        else:

            if User.objects(email=user_data["email"]).count() != 0:
                users = User._get_collection()
                users.find_one_and_update({"email": user_data["email"]}, {"$set": user_data})
                user_data.clear()
            else:
                try:
                    User(**user_data).save()
                    user_data.clear()
                    bot.send_message(message.chat.id, "Data is stored. Thank you!")
                except ValidationError as err:
                    bot.send_message(message.chat.id, f"Data was not stored! {err}")

    except IndexError:
        bot.send_message(message.chat.id, "Data is stored. Thank you!")


if __name__ == "__main__":
    bot.polling()