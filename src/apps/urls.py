from flask import Blueprint
from .views import *
import os, sys

app_name = __name__

exec(
    '''
{0} = Blueprint("{0}", __name__)
{0}.add_url_rule('/', 'app', app)
    '''.format(app_name[:app_name.rfind('.', 0, app_name.rfind('/'))])
)
