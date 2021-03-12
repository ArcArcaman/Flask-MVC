import redis
from flask import Flask

__temp_app = Flask(__name__)

__temp_app.config.from_pyfile('../../config.cfg')

config = __temp_app.config

__connections = config['REDIS_CONNECTIONS']

REDIS = {}

for connection, params in __connections.items():
    REDIS[connection] = redis.Redis(**params)
    if(config['DEBUG'] == True): print(" * Redis Connection Test {" + connection + "}:", 'OK' if REDIS[connection].ping() else 'PING FAIL')