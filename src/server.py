from importlib import import_module

from flask import Flask

from flask_wtf.csrf import CSRFProtect

from flask_cors import CORS

import utils
import sys, os

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

#Create SECRET_KEY if not exist
if app.secret_key == None:
    app.secret_key = utils.generateSecKey()

if app.config.get("ROOT_NAME") == None:
    app.config["ROOT_NAME"] = '/'

#Get your app names
if app.config.get("APPS") == None:
    app.config["APPS"] = ['root']
moduleNames = app.config["APPS"]

if app.config.get("CORS_EN") == None:
    app.config["CORS_EN"] = False

if app.config.get("CORS_EN") == True:
    CORS(app)

if app.config.get("CSRF_EN") == None:
    app.config["CSRF_EN"] = False

if app.config.get("CSRF_EN") == True:
    CSRFProtect().init_app(app)

#Support for Regex Convertion in URL Routing
app.url_map.converters['regex'] = utils.RegexConverter

# imports all listed extensions
extensions = app.config.get('EXTENSIONS')
if extensions != None:
    for extension in extensions:
        globals()['extensions.' + extension] = import_module('extensions.' + extension)

for module in moduleNames:
    globals()[module] = import_module(module)

for module in moduleNames:
    if module != 'root':
        app.register_blueprint(getattr(globals()[module].urls, module), url_prefix=app.config["ROOT_NAME"] + module, template_folder=module)
    else:
        app.register_blueprint(getattr(root.urls, "root"), url_prefix=app.config["ROOT_NAME"], template_folder='root')

if __name__ == "__main__":
    if(app.config["DEBUG"]==True): print(" * ROOT_NAME: {0}".format(app.config["ROOT_NAME"]))

    if app.config.get("HOST") != None and app.config.get("PORT") != None:
        app.run(host=app.config["HOST"], port=app.config["PORT"])
    elif app.config.get("HOST") == None and app.config.get("PORT") != None:
        app.run(host="localhost", port=app.config["PORT"])
    elif app.config.get("HOST") != None and app.config.get("PORT") == None:
        app.run(host=app.config["HOST"], port=5000)
    else:
        app.run(host="localhost", port=5000)