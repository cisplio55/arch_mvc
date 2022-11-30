from flask import Flask
# Controller Blue print imports.
from src.authantication.controller import *
from src.products.controller import *
from src.order.controller import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from yml_handler.flask_route_to_swagger import generate_swagger_yaml
from util import dataresponse, errorresponse
from flask import Flask, render_template, request
from yaml.loader import SafeLoader
from flask import Response
import io
import yaml
from yml_handler.swagger_yaml_to_excell import *
from yml_handler.flask_route_to_swagger import *
from mongoengine import *
from util import DB_URI
import click

from src.authantication.controller import *


connect(host=DB_URI)   # Provide database connection to mongo engene.

app = Flask(
    __name__,
    template_folder='frontend',
    static_url_path=None, #'/static',
    static_folder='frontend',
)




# -----------------------------------------------------------------------------------------
# JWT authentication.
# -----------------------------------------------------------------------------------------
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
# -----------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------
# Bind controllers,
# -----------------------------------------------------------------------------------------
app.add_url_rule("/root/authentication/register",  view_func=Register_con().register, methods = ['POST'])
app.add_url_rule("/root/authentication/login",  view_func=Login_con().login, methods = ['POST'])
app.add_url_rule("/root/product/create_product",  view_func=Create_product_con().create_product, methods = ['POST'])
app.add_url_rule("/root/product/add_to_cart",  view_func=Add_to_cart_con().add_to_cart, methods = ['POST'])
app.add_url_rule("/root/product/get_product_details/<int:product_id>/<string:product_name>/<user_name>", view_func=Get_product_details_con().get_product_details, methods = ['GET', 'POST'])
# -----------------------------------------------------------------------------------------


@app.cli.command("exportcsv")
@click.argument("sheetid")
def exportcsv(sheetid):
    # flask exportcsv 1XZEQQ8WzhnlY-A22uiUuiHv0OX0TlNeON9lFTszFkLs
    try:
        service_file_path = "/Users/codeclouds-subhankar/Desktop/subhankar/projects/Tutorial/python_basics/flask/arch_mvc/t-pulsar-369511-2b54d807cd19.json"
        spreadsheet_id = sheetid #"1XZEQQ8WzhnlY-A22uiUuiHv0OX0TlNeON9lFTszFkLs"
        sheet_name = "swagger-yaml-to-table"
        df = yml_to_df(app, data=version20().generate_swagger_yaml(app))
        print(write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, df))
    except Exception as e:
        traceback.print_exc()


# -----------------------------------------------------------------------------------------
# Show Route urls
# -----------------------------------------------------------------------------------------
print("------------------------------------")
print("         Routing paths")
print("------------------------------------")
rules = [str(rule) for rule in app.url_map.iter_rules()]
rules.sort()
for rule in rules:
   print(str(rule))
print("------------------------------------")
# -----------------------------------------------------------------------------------------





if __name__ == "__main__":
    app.run(debug=True)
