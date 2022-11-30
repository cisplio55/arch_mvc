
from mongoengine import *

class Register(Document):
    username = StringField(required=True, max_length=20)
    password = StringField(required=True, max_length=100)
    email    = StringField(required=True, max_length=50)
    phone    = StringField(required=False, max_length=10)

    register_schema = {
        "type" : "object",
        "properties" : {
            "username"  : {"type" : "string", "minLength": 5, "maxLength": 20},
            "password"  : {"type" : "string", "minLength": 5, "maxLength": 100},
            "email"     : {"type" : "string", "maxLength": 50},
            "phone"     : {"type" : "string", "maxLength": 10},
        },
        "required": ["username", "password", "email"]
    }

    login_schema = {
        "type" : "object",
        "properties" : {
            "username"  : {"type" : "string", "minLength": 5, "maxLength": 20},
            "password"  : {"type" : "string", "minLength": 5, "maxLength": 100},
        },
        "required": ["username", "password"]
    }




