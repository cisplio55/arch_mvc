
from mongoengine import *
from src.authantication.models import Register
from util import generate_uid

class Product(Document):
    product_name = StringField(required=True, max_length=30)
    product_desc = StringField(required=False, max_length=500)
    product_price = FloatField(required=True, min_value=1)
    is_featured = BooleanField(required=False)
    created_by = ReferenceField(
        Register, required=True, reverse_delete_rule=CASCADE)

    create_product_schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "minLength": 5, "maxLength": 30},
            "product_desc": {"type": "string", "minLength": 5, "maxLength": 500},
            "product_price": {"type": "number"},
            "is_featured": {"type": "boolean", "maxLength": 10},
        },
        "required": ["product_name", "product_price"]
    }


class Cart(Document):
    user = ReferenceField(Register, required=True, reverse_delete_rule=CASCADE)
    product = ReferenceField(Product, required=True,
                             reverse_delete_rule=CASCADE)
    count = IntField(min_value=1)

    add_to_cart_schema = {
        "type": "object",
        "properties": {
            "product_id": {"type": "string", "minLength": 24, "maxLength": 30},
        },
        "required": ["product_id"]
    }

# print(Cart.add_to_cart_schema)

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
