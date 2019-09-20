from flask import Flask
import yaml, os

__temp_app = Flask(__name__)

__temp_app.config.from_pyfile('config.cfg')

FLASK_CONFIG = __temp_app.config

USER_GLOBAL = None

if FLASK_CONFIG.get("USER_GLOBAL_FILE") != None:
    if os.path.isfile(FLASK_CONFIG["USER_GLOBAL_FILE"]):
        if FLASK_CONFIG["USER_GLOBAL_FILE"].endswith('.yml') or FLASK_CONFIG["USER_GLOBAL_FILE"].endswith('.yaml'):
            with open(FLASK_CONFIG["USER_GLOBAL_FILE"]) as source:
                USER_GLOBAL = yaml.load(source, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("USER_GLOBAL_FILE must be a YAML file.")