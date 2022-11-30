from flask import Blueprint
from util import *
from flask import request
from .models import Register
import bcrypt
from flask_jwt_extended import create_access_token
from .models import *


class Register_con:
    def __init__(self):
        self.model = Register

    def register(self):
        try:
            enteredInfo = getenteredInfo(request)
            obj = self.model.objects(username=enteredInfo.get("username"))
            if list(obj) != []:
                return errorresponse("register", "", message="Username already exists. Please login")
            enteredInfo["password"]=bcrypt.hashpw(enteredInfo.get("password").encode('utf-8'), bcrypt.gensalt())
            obj = self.model(**enteredInfo)
            obj.save()
            return dataresponse("register", {"message" : "Thanks for register."})
        except Exception as e:
            return errorresponse("register", e)

    def get_schema(self):
        return self.model.register_schema





class Login_con:
    def __init__(self):
        self.model = Register
        
    def login(self):
        try:
            enteredInfo = getenteredInfo(request)
            obj = self.model.objects(username=enteredInfo.get("username")).first()
            if bcrypt.checkpw(enteredInfo.get("password").encode('utf-8'), obj.password.encode('utf-8')):
                access_token = create_access_token(identity=str(obj.id))
                return dataresponse("login", {"message": "Login Successful", "access_token": access_token})
            return dataresponse("login", {"message": "Invalid credential"})

        except Exception as e:
            return errorresponse("register", e)

    def get_schema(self):
        return self.model.login_schema

