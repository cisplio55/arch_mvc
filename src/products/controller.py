from flask import Blueprint
from util import *
from flask import request
from .models import Product
from src.authantication.models import Register
from .models import Product, Cart
import bcrypt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

product_controller = Blueprint("product", __name__)

@product_controller.route('/product/create_product', methods = ["POST"])
@jwt_required(fresh=False)
def create_product():
    try:
        enteredInfo = getenteredInfo(request)
        print(enteredInfo)
        product = Product(
            product_name    =  enteredInfo.get("product_name"),
            product_desc    =  enteredInfo.get("product_desc"),
            product_price   =  enteredInfo.get("product_price"),
            is_featured     =  enteredInfo.get("is_featured"),
            created_by      =  Register.objects.get(pk=get_jwt_identity()),
        )
        product.save()
        return dataresponse("product", {"message" : "Product added successfully."})
    except Exception as e:
        return errorresponse("register", e)


@product_controller.route('/product/add_to_cart', methods = ["POST"])
@jwt_required(fresh=False)
def add_to_cart():
    try:
        enteredInfo = getenteredInfo(request)
        product_id = enteredInfo.get("product_id")
        user_id = get_jwt_identity()
        
        cart_item = Cart.objects(product = product_id, user = user_id)

        if cart_item.count() == 0:
            cart = Cart(
                product =  Product.objects.get(pk=product_id),
                user    =  Register.objects.get(pk=user_id),
                count   = 1
            )
            cart.save()
        else:
            cart_item.update_one(inc__count=1)
            return dataresponse("add_to_cart", {"message" : "Cart item incremented by one."})
            
        return dataresponse("add_to_cart", {"message" : "Product added to cart."})
    except Exception as e:
        return errorresponse("add_to_cart", e)



