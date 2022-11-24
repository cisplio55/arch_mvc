from flask import Flask
# Controller Blue print imports.
from src.authantication.controller import *
from src.products.controller import *
from src.order.controller import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from yml_handler.flask_route_to_swagger import generate_swagger_yaml
from util import dataresponse, errorresponse
from flask import Flask, render_template, request
from yaml.loader import SafeLoader
from flask import Response
import io
import yaml
from yml_handler.swagger_yaml_to_excell import *
from mongoengine import *
from util import DB_URI

connect(host=DB_URI)   # Provide database connection to mongo engene.

app = Flask(
    __name__,
    template_folder='frontend',
    static_url_path='/static',
    static_folder='frontend',
)



import click




# -----------------------------------------------------------------------------------------
# JWT authentication.
# -----------------------------------------------------------------------------------------
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
# -----------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------
# Bind controllers,
# -----------------------------------------------------------------------------------------
app.add_url_rule("/root/authentication/register",  view_func=register, methods = ['POST'])
app.add_url_rule("/root/authentication/login",  view_func=login, methods = ['POST'])
app.add_url_rule("/root/product/create_product",  view_func=create_product, methods = ['POST'])
app.add_url_rule("/root/product/get_product_details/<int:product_id>/<string:product_name>/<user_name>",  view_func=get_product_details, methods = ['GET', 'POST'])
app.add_url_rule("/root/product/add_to_cart",  view_func=add_to_cart, methods = ['POST'])
# -----------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------
# Make sure yml_handler directory is available with app.py file.
# Swagger utility functions, Just copy this block of code in any project
# All the imports are capt in this block for easy portability.
# -----------------------------------------------------------------------------------------
# from flask import Flask, render_template, request
# from yaml.loader import SafeLoader
# from flask import Response
# import io
# import yaml
# from yml_handler.swagger_yaml_to_excell import *


@app.cli.command("exportcsv")
@click.argument("sheetid")
def exportcsv(sheetid):
    try:
        service_file_path = "/Users/codeclouds-subhankar/Desktop/subhankar/projects/Tutorial/python_basics/flask/arch_mvc/t-pulsar-369511-2b54d807cd19.json"
        spreadsheet_id = sheetid #"1XZEQQ8WzhnlY-A22uiUuiHv0OX0TlNeON9lFTszFkLs"
        sheet_name = "swagger-yaml-to-table"
        df = yml_to_df(app, data=generate_swagger_yaml(app))
        print(write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, df))
    except Exception as e:
        traceback.print_exc()


@app.route('/')
def upload_File_page(name=None):  # To return the file upload UI.
    return render_template('uploadFile.html', name=name)

@app.route('/utility/swagger/UI/generate_csv_data', methods=['POST'])
def generate_csv_data():
    try:
        rettype = request.form.to_dict(flat=False).get("rettype", ["CSV"])[0].upper()
        raw_data = request.files['file'].read()
        data = yaml.load(raw_data, Loader=SafeLoader)
        df = yml_to_df(app, data)
        fileName = "OutputTable"

        if rettype == "CSV":
            """This block Returns CSV file"""
            s   = io.StringIO()
            df.to_csv(s, index=False)
            csv = s.getvalue()
            response = make_response(csv)
            cd = 'attachment; filename={}.csv'.format(fileName)
            response.headers['Content-Disposition'] = cd
            response.mimetype='text/csv'
            return response
        elif rettype == "EXCEL":
            """This block returns Excel file"""
            buffer = io.BytesIO()
            total_style = pd.Series("font-weight: bold;", index=["Response Code"])
            df.style.apply(lambda s: total_style)
            df.to_excel(fileName+".xlsx", index=False)
            df.to_excel(buffer, index=False)
            headers = {
                'Content-Disposition': 'attachment; filename={}.xlsx'.format(fileName),
                'Content-type': 'application/vnd.ms-excel'
            }
            return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)

    except Exception as e:
        return errorresponse("get_csv_data", e)


@app.route("/utility/swagger/UI/generate_yaml")
def generate_yaml():
    try:
        generate_swagger_yaml(app)
        return dataresponse("generate_yaml", {"mesage" : "Swagger YAML file generated successfully"})
    except Exception as e:
        errorresponse("generate_yaml", e)
# generate_swagger_yaml(app) # Create swagger file automatically on flask run.
# ----------------------------------------------------------------------------



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
