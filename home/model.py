from mongoengine import *
connect("telegram_users")


class User(Document):
    name = StringField(required=True, max_length=255)
    surname = StringField(required=True, max_length=255)
    phone_number = StringField(max_length=20)
    email = EmailField()
    address = StringField(max_length=255)
    wishes = StringField(max_length=4096)

    @classmethod
    def get_fields(cls):
        return ["name", "surname", "phone_number", "email", "address", "wishes"]
