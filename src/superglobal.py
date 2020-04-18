from flask import Flask
import yaml, os
from importlib import import_module

__temp_app = Flask(__name__)

__temp_app.config.from_pyfile('config.cfg')

FLASK_CONFIG = __temp_app.config

EXTENSIONS = dict() if FLASK_CONFIG.get('EXTENSIONS') != None else None
for extension in FLASK_CONFIG.get('EXTENSIONS'):
    extension_path = os.path.join(os.path.dirname(__file__), 'extensions', extension)
    if os.path.isdir(extension_path):
        if os.path.isfile(extension_path + '/global.yml'):
            with open(extension_path + '/global.yml', 'r') as source:
                EXTENSIONS[extension] = dict()
                loaded = yaml.load(source, Loader=yaml.FullLoader)
                __temp = import_module('extensions.' + extension)
                for var in loaded:
                    if type(var) == dict:
                        EXTENSIONS[extension][list(var.keys())[0]] = var[list(var.keys())[0]]
                    elif type(var) == str:
                        EXTENSIONS[extension][var] = getattr(__temp, var)
                    else:
                        raise TypeError("Unknown variable type in global of extensions/" + extension + ". Please contact the respective developer of the extension.")
    else:
        raise FileNotFoundError("Extension " + extension + " not found.")
                        

USER_GLOBAL = None

if FLASK_CONFIG.get("USER_GLOBAL_FILE") != None:
    if os.path.isfile(FLASK_CONFIG["USER_GLOBAL_FILE"]):
        if FLASK_CONFIG["USER_GLOBAL_FILE"].endswith('.yml') or FLASK_CONFIG["USER_GLOBAL_FILE"].endswith('.yaml'):
            with open(FLASK_CONFIG["USER_GLOBAL_FILE"]) as source:
                USER_GLOBAL = yaml.load(source, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("USER_GLOBAL_FILE must be a YAML file.")