import yaml
import re
import traceback
import inspect
from undecorated import undecorated

base_format = {
    'swagger': '2.0',
    'info': {
        'description': 'Pypa API specification, across all products.',
        'title': 'Pypa Endpoint for Development',
        'version': '1.0.0'
    },
    'host': 'pypa-api-development.endpoints.huko-312103.cloud.goog',
    'x-google-endpoints': [
        {
            'name': 'pypa-api-development.endpoints.huko-312103.cloud.goog',
            'target': '34.149.86.33'
        }
    ],
    'consumes': [
        'application/json'
    ],
    'produces': [
        'application/json'
    ],
    'schemes': [
        'https',
        'http'
    ],
    'security': [
        {
            'api_key': [],
            'pypa_auth': []
        }
    ],
    'paths': {},
    'securityDefinitions': {
        'api_key': {
            'type': 'apiKey',
            'name': 'x-api-key',
            'in': 'header'
        },
        'pypa_auth': {
            'authorizationUrl': '',
            'flow': 'implicit',
            'type': 'oauth2',
            'x-google-issuer': 'development-endpoint-service@huko-312103.iam.gserviceaccount.com',
            'x-google-jwks_uri': 'https: //www.googleapis.com/service_accounts/v1/metadata/x509/development-endpoint-service@huko-312103.iam.gserviceaccount.com',
            'x-google-audiences': 'pypa-api-development.endpoints.huko-312103.cloud.goog'
        }
    }
}


def rm_sc_make_title(str):
    return re.sub('[^a-zA-Z0-9 \n\.]', ' ', str).title()


def CreateSwaggerSpecificRoute(rule):
    route_path = str(rule)   # /multi/level/url/test/{user_id}/{org_id}
    for s in re.findall(r'[^<]+:', str(rule)):
        route_path = route_path.replace(s, "")
    route_path = route_path.replace("<", "{")
    route_path = route_path.replace(">", "}")
    return route_path


def CreateSwaggerSpecificParameterArray(rule):
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


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def generate_swagger_yaml(app):
    try:
        for rule in app.url_map.iter_rules():
            # print('map', rule.map)
            # print('arguments',  rule.arguments)
            # print('bind',  str(rule.bind))
            # print('build',  str(rule.build))
            # print('build_compare_key',  str(rule.build_compare_key))
            # print('build_only',  rule.build_only)
            # print('compile',  str(rule.compile))
            # print('defaults',  rule.defaults)
            # print('empty',  str(rule.empty))
            # print('endpoint',  rule.endpoint)
            # print('get_converter',  str(rule.get_converter))
            # print('get_empty_kwargs',  str(rule.get_empty_kwargs))
            # print('get_rules',  rule.get_rules)
            # print('host',  rule.host)
            # print('methods',  rule.methods)
            # print('provide_automatic_options',  rule.provide_automatic_options)
            # print('provides_defaults_for',  str(rule.provides_defaults_for))
            # print('redirect_to',  rule.redirect_to)
            # print('refresh',  str(rule.refresh))
            # print('rule',  str(rule.rule))
            # print('strict_slashes',  rule.strict_slashes)
            # print('subdomain',  rule.subdomain)
            # print('suitable_for',  str(rule.suitable_for))
            # print('websocket', rule.websocket)
            # print("**************************************")

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
            route_path = CreateSwaggerSpecificRoute(rule)
            # Create a parameter array from rule
            parameter_names = CreateSwaggerSpecificParameterArray(rule) # list(rule.arguments) # has to replace it
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
                        
                        default_schema = get_default_args(undecorated(app.view_functions[endpoint])).get("schema")
                        # default_schema = inspect.getcallargs(undecorated(app.view_functions[endpoint])).get("schema")
                        body_parameters = [
                            {
                                "in": "body",
                                "name": ep_as_desc,
                                "description": description,
                                # rule.defaults.get("schema") if rule.defaults is not None else {} #rule.defaults#rv.get_json() if "properties" in rv.get_json() else {},
                                "schema": default_schema or {}
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
            base_format["paths"].update({route_path: route_format})

            with open(output_yaml_file, 'w') as f:
                data = yaml.dump(base_format, f)


        # -------------------------------------------------
        # Modify the router path to keep inside quotation
        # -------------------------------------------------
        data = None
        with open(output_yaml_file, 'r') as file:
            data = file.read()
        for rule in app.url_map.iter_rules():
            route_path = CreateSwaggerSpecificRoute(rule)
            data = data.replace(route_path+":", '"'+route_path+'":')
        with open(output_yaml_file, 'w') as file:
            file.write(data)
        # -------------------------------------------------


        return True
    except Exception as e:
        traceback.print_exc()
        return None
