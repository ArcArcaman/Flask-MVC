import os, base64
from werkzeug.routing import BaseConverter

#print(base64.b64encode(os.urandom(64)).decode('utf-8'))

def generateSecKey():
    return base64.b64encode(os.urandom(64)).decode('utf-8')

class RegexConverter(BaseConverter):
    def __init__(self, url, *regx):
        super(RegexConverter, self).__init__(url)
        self.regex = regx[0]
