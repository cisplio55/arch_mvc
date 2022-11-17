from flask import Blueprint
from util import *
from flask import request
from .models import Register
import bcrypt
from flask_jwt_extended import create_access_token
from .schema import *

auth_controller = Blueprint("authentication", __name__)

@auth_controller.route('/authentication/register', methods = ["POST"], defaults={'schema': register_schema})
def register(schema):
    try:
        enteredInfo = getenteredInfo(request)
        obj = Register.objects(username=enteredInfo.get("username"))
        if list(obj) != []:
            return errorresponse("register", "", message="Username already exists. Please login")
        enteredInfo["password"]=bcrypt.hashpw(enteredInfo.get("password").encode('utf-8'), bcrypt.gensalt())
        obj = Register(**enteredInfo)
        obj.save()
        return dataresponse("register", {"message" : "Thanks for register."})
    except Exception as e:
        return errorresponse("register", e)

@auth_controller.route('/authentication/login', methods = ["POST"], defaults={'schema': login_schema})
def login(schema):
    try:
        enteredInfo = getenteredInfo(request)
        obj = Register.objects(username=enteredInfo.get("username")).first()
        if bcrypt.checkpw(enteredInfo.get("password").encode('utf-8'), obj.password.encode('utf-8')):
            access_token = create_access_token(identity=str(obj.id))
            return dataresponse("login", {"message": "Login Successful", "access_token": access_token})
        return dataresponse("login", {"message": "Invalid credential"})

    except Exception as e:
        return errorresponse("register", e)
