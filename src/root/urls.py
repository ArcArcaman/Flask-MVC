from flask import Blueprint
from .views import *

root = Blueprint("root", __name__)

root.add_url_rule('/', 'index', index)
