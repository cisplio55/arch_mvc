from flask import Blueprint
from util import *
from flask import request
from .models import Order
from src.products.models import Cart
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

order_controller = Blueprint("order", __name__)

@order_controller.route('/order/place_order', methods = ["POST"])
@jwt_required(fresh=False)
def place_order():
    try:
        enteredInfo = getenteredInfo(request)
        cart_data = Cart.objects(user=get_jwt_identity())

        #TODO Implimentation under process.
        # Order(
        #     order_price     =   "",
        #     dlivery_address =   "",
        #     order_status    =   "",
        #     paymentmode     =   "",
        #     product_detail  =   "",
        #     created_by      =   ""
        # )
        # order.save()
        return dataresponse("product", {"data" : "cart_data", "message" : "Order placed successfully."})
    except Exception as e:
        return errorresponse("register", e)
