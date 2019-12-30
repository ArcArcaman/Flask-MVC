from flask import Blueprint
from .views import *
import os, sys
import yaml

app_name = __name__

directory = app_name[:app_name.rfind('.', 0, app_name.rfind('/'))]

exec(
    '{0} = Blueprint("{0}", __name__)'.format(directory)
)

urls_source_path = ''

if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'urls.yml')):
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'urls.yaml')):
        raise FileNotFoundError("'urls' yaml configuration file not exist in current directory.")
    else: urls_source_path = os.path.join(os.path.dirname(__file__), 'urls.yaml')
else: urls_source_path = os.path.join(os.path.dirname(__file__), 'urls.yml')

with open(urls_source_path) as source:
    urls_setting = yaml.load(source, Loader=yaml.FullLoader)

    for endpoint, details in urls_setting.items():
        if details.get('options') == None:
            exec(
                "{0}.add_url_rule('{rule}', '{endpoint}', {view})".format(directory, rule=details['rule'], endpoint=endpoint, view=details['view'])
            )
        else:
            exec(
                "{0}.add_url_rule('{rule}', '{endpoint}', {view}, **{options})".format(directory, rule=details['rule'], endpoint=endpoint, view=details['view'], options=details['options'])
            )
