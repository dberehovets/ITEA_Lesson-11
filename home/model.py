from mongoengine import *
connect("telegram_users")


class User(Document):
    name = StringField(default=None, max_length=255)
    surname = StringField(default=None, max_length=255)
    phone_number = StringField(default=None, max_length=20)
    email = EmailField(default=None)
    address = StringField(default=None, max_length=255)
    wishes = StringField(default=None, max_length=4096)
    telegram_id = IntField()

    def get_fields(self):
        return {"name": self.name,
                "surname": self.surname,
                "phone_number": self.phone_number,
                "email": self.email,
                "address": self.address,
                "wishes": self.wishes
                }
