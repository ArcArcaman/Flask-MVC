from mongoengine import *

# Connect to MongoDB
connect(
    alias = 'db_alias',
    host = 'mongodb://localhost',
    port = 27017
)