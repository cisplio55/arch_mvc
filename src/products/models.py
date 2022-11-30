
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
        "type" : "object",
        "properties" : {
            "product_id"  : {"type" : "string", "minLength": 5, "maxLength": 20},
        },
        "required": ["product_id"]
    }