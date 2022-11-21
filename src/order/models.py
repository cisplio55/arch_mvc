
from mongoengine import *
from src.authantication.models import Register

class Order(Document):
    order_price     = FloatField(required=True, min_value=1)
    dlivery_address = StringField(required=True, max_length=30)
    order_status    = BooleanField(required=False)
    paymentmode     = StringField(required=True, max_length=30)
    product_detail  = ListField()
    created_by      = ReferenceField(Register, required=True, reverse_delete_rule=CASCADE)
