from flask import Flask
# Controller Blue print imports.
from src.authantication.controller import *
from src.products.controller import *
from src.order.controller import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from yml_handler.flask_route_to_swagger import generate_swagger_yaml
from util import dataresponse, errorresponse

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

# -----------------------------------------------------------------------------------------
# Generate swagger UI file.
# -----------------------------------------------------------------------------------------
@app.route("/utility/swagger/UI/generate_yaml")
def generate_yaml():
    try:
        generate_swagger_yaml(app)
        return dataresponse("generate_yaml", {"mesage" : "Swagger YAML file generated successfully"})
    except Exception as e:
        errorresponse("generate_yaml", e)
# generate_swagger_yaml(app) # Create swagger file automatically on flask run.
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# Bind controllers
# -----------------------------------------------------------------------------------------
app.add_url_rule("/root/authentication/register",  view_func=register, methods = ['POST'])
app.add_url_rule("/root/authentication/login",  view_func=login, methods = ['POST'])
app.add_url_rule("/root/product/create_product",  view_func=create_product, methods = ['POST'])
app.add_url_rule("/root/product/add_to_cart",  view_func=add_to_cart, methods = ['POST'])
# -----------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# Show Route urls
# -----------------------------------------------------------------------------------------
for rule in app.url_map.iter_rules():
   print(str(rule))
# -----------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
    