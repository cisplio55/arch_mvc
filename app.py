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


from yml_handler.flask_route_to_swagger import generate_swagger_yaml
from util import dataresponse, errorresponse
@app.route("/utility/swagger/UI/generate_yaml")
def generate_yaml():
    try:
        generate_swagger_yaml(app)
        return dataresponse("generate_yaml", {"mesage" : "Swagger YAML file generated successfully"})
    except Exception as e:
        errorresponse("generate_yaml", e)
# generate_swagger_yaml(app) # Create swagger file automatically on flask run.




for rule in app.url_map.iter_rules():
   print(str(rule))
if __name__ == "__main__":
    app.run(debug=True)


