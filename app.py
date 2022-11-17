from flask import Flask
# Controller Blue print imports.
from src.authantication.controller import auth_controller
from src.products.controller import product_controller
from src.order.controller import order_controller

app = Flask(__name__)
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

# Controller blueprint register.
app.register_blueprint(auth_controller, url_prefix="/root")
app.register_blueprint(product_controller, url_prefix="/root")
app.register_blueprint(order_controller, url_prefix="/root")


for rule in app.url_map.iter_rules():
   print(str(rule))
if __name__ == "__main__":
    app.run(debug=True)


