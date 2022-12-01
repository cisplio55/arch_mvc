import yaml
import re
import traceback
import inspect
from undecorated import undecorated
from abc import ABC, abstractmethod
import importlib

base_format_v20 = { 'swagger': '2.0', 'info': { 'description': 'Pypa API specification, across all products.', 'title': 'Pypa Endpoint for Development', 'version': '1.0.0' }, 'host': 'pypa-api-development.endpoints.huko-312103.cloud.goog', 'x-google-endpoints': [ { 'name': 'pypa-api-development.endpoints.huko-312103.cloud.goog', 'target': '34.149.86.33' } ], 'consumes': [ 'application/json' ], 'produces': [ 'application/json' ], 'schemes': [ 'https', 'http' ], 'security': [ { 'api_key': [], 'pypa_auth': [] } ], 'paths': {}, 'securityDefinitions': { 'api_key': { 'type': 'apiKey', 'name': 'x-api-key', 'in': 'header' }, 'pypa_auth': { 'authorizationUrl': '', 'flow': 'implicit', 'type': 'oauth2', 'x-google-issuer': 'development-endpoint-service@huko-312103.iam.gserviceaccount.com', 'x-google-jwks_uri': 'https: //www.googleapis.com/service_accounts/v1/metadata/x509/development-endpoint-service@huko-312103.iam.gserviceaccount.com', 'x-google-audiences': 'pypa-api-development.endpoints.huko-312103.cloud.goog' } } }
# base_format_v30 = {"paths" : {}}

def rm_sc_make_title(str):
    return re.sub('[^a-zA-Z0-9 \n\.]', ' ', str).title()

 

class Swagger(ABC):
    def CreateSwaggerSpecificRoute(self, rule):
        route_path = str(rule)   # /multi/level/url/test/{user_id}/{org_id}
        for s in re.findall(r'[^<]+:', str(rule)):
            route_path = route_path.replace(s, "")
        route_path = route_path.replace("<", "{")
        route_path = route_path.replace(">", "}")
        return route_path

    def CreateSwaggerSpecificParameterArray(self, rule):
        replacement = {"int":"integer"}
        parameter_names = []#[s.replace(">", "") for s in re.findall(r'[^<]+>', str(rule))]
        for s in re.findall(r'[^<]+>', str(rule)):
            s = s.replace(">", "")
            if ":" in s:   # "type:param_name"
                param = list(s.split(":"))
                if param[0] in replacement.keys(): # Replace the type with swagger specific keword. e.g. int > integer
                    param[0] = replacement[param[0]]
                parameter_names.append(param)
            else:
                parameter_names.append(("string",s))
        return parameter_names

    def get_default_args(self, func):
        signature = inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

    def get_schema(self, app, endpoint):
        controller_method = app.view_functions[endpoint]
        controller_class =  controller_method.__self__.__class__()
        # -----------------------------
        #using import module.
        # -----------------------------
        # controller_module = controller_method.__module__
        # controller_class_name = controller_class.__class__.__name__
        # module = importlib.import_module(controller_module)
        # my_class = getattr(module, controller_class_name)
        # my_instance = my_class()
        # -----------------------------
        default_schema = controller_class.get_schema() if "get_schema" in dir(controller_class) else {}
        return default_schema
                            


    @abstractmethod
    def generate_swagger_yaml():
        pass


class Version20(Swagger):
    def __init__(self, base_format = base_format_v20):
        self.base_format = base_format

    def generate_swagger_yaml(self, app):
        try:
            for rule in app.url_map.iter_rules():
                # Do not include static urls. So just skip if the there is static rule.
                if rule.endpoint == "static":
                    continue
                
                # -----------------------------------
                # Get the router Path and param name and make the swagger specific formet.
                # -----------------------------------
                route_format = {}
                verb_details = {}
                body_parameters = []
                output_yaml_file = "swagger.yaml"
                endpoint = rule.endpoint
                desc_200 = {"description": "Success"}
                route_path = self.CreateSwaggerSpecificRoute(rule)
                # Create a parameter array from rule
                parameter_names = self.CreateSwaggerSpecificParameterArray(rule) # list(rule.arguments) # has to replace it
                # -----------------------------------

                description = rm_sc_make_title(route_path)  # Make a description
                ep_as_desc = rm_sc_make_title(endpoint)
                option_details = {  # Do this block when parameter is availabe.
                    'description': ep_as_desc,
                    "summary": ep_as_desc,
                    # 'operationId': uuid.uuid4().hex,#'authentication-post-permissions-delete',
                    'produces': ['application/json'],
                    'responses': {
                        200: desc_200
                    },
                    'security': [
                        {
                            'api_key': [],
                            'pypa_auth': []
                        }
                    ]
                }

                param_array = [{
                    'name': param[1],  # Get the first parameter from url
                    'in': 'path',
                    'description': "Input for " + param[1],
                    'required': True,
                    'type': param[0]
                } for param in parameter_names] if parameter_names != [] else []

                http_verbs = ["get", "post", "patch", "put", "delete"]
                for method in http_verbs:
                    if method.upper() in rule.methods:
                        # ----------------------------------------------
                        # Prepare the body with schema.
                        # ----------------------------------------------
                        if method != "get":
                            default_schema = self.get_schema(app, endpoint)
                            body_parameters = [
                                {
                                    "in": "body",
                                    "name": ep_as_desc,
                                    "description": description,
                                    "schema": default_schema
                                }
                            ]
                        # ----------------------------------------------

                        verb_details.update({method: {
                            "summary": ep_as_desc,
                            "consumes": [
                                "application/json"
                            ],
                            # Add URL parameters.
                            "parameters": param_array+body_parameters,
                            "responses": {
                                200: desc_200
                            }
                        }
                        })

                        option_details.update(
                            {"parameters": param_array+body_parameters})

                route_format.update(verb_details)
                route_format["options"] = option_details       # Update parameters

                # {"/accounts/.../view/{doc_id}" : {...}}
                self.base_format["paths"].update({route_path: route_format})

                with open(output_yaml_file, 'w') as f:
                    data = yaml.dump(self.base_format, f)


            # -------------------------------------------------
            # Modify the router path to keep inside quotation
            # -------------------------------------------------
            data = None
            with open(output_yaml_file, 'r') as file:
                data = file.read()
            for rule in app.url_map.iter_rules():
                route_path = self.CreateSwaggerSpecificRoute(rule)
                data = data.replace(route_path+":", '"'+route_path+'":')
            with open(output_yaml_file, 'w') as file:
                file.write(data)
            # -------------------------------------------------
            return yaml.load(data)

        except Exception as e:
            traceback.print_exc()
            return None

# class version30(Version20):
#     def __init__(self, base_format=base_format_v30):
#         self.base_format = base_format
        
