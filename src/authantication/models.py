
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



# from abc import ABC, abstractmethod
# from flask import request
# from util import *
# import bcrypt
# from src.db_if import mongodb
# from util import logger
# # ----------------------------
# # interface segrigation for different user interface like guest user, normal user, admin user.
# # ----------------------------
# class signup_interface(ABC):
#     @abstractmethod
#     def signup(self):
#         pass

# class signin_interface(ABC):
#     @abstractmethod
#     def signin(self):
#         pass
# # ----------------------------

# class normal_user(signup_interface, signin_interface, mongodb):
    
#     def signup(self):
#         try:
#             enteredInfo = getenteredInfo(request)

#             signup_form = {
#                 "username"  : enteredInfo.get("username"),
#                 "password"  : bcrypt.hashpw(enteredInfo.get("password").encode('utf-8'), bcrypt.gensalt()),
#                 "email"     : enteredInfo.get("email"),
#             }

#             collection = mongodb().get_collection("userCredential")
#             user = collection.find_one({"username": signup_form.get("username")})
#             if user == None:
#                 # mongodb().save("userCredential", signup_form)
#                 collection.insert_one(signup_form)
#                 return {"message": "Thanks for Signup."}
#             else:
#                 return {"message": "User already exists. Please login or try with another user name."}

#         except Exception as e:
#             logger("signup", e, level="error")
#             return None

#     def signin(self):
#         print("user.signin")



# class user_profile(signup_interface):

#     def __init__(self):
#         pass

#     def get_user_profile(self):
#         pass

#     def update_user_profile(self):
#         pass




