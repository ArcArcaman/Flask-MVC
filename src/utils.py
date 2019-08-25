import os, base64

#print(base64.b64encode(os.urandom(64)).decode('utf-8'))

def generateSecKey():
    return base64.b64encode(os.urandom(64)).decode('utf-8')