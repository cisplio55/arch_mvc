


create_product_schema = {
    "type" : "object",
    "properties" : {
        "product_name"  : {"type" : "string", "minLength": 5, "maxLength": 30},
        "product_desc"  : {"type" : "string", "minLength": 5, "maxLength": 100},
        "product_price"     : {"type" : "number"},
        "is_featured"     : {"type" : "boolean", "maxLength": 10},
    },
    "required": ["product_name", "product_price"]
}

add_to_cart_schema = {
    "type" : "object",
    "properties" : {
        "product_id"  : {"type" : "string", "minLength": 24, "maxLength": 30},
    },
    "required": ["product_id"]
}
