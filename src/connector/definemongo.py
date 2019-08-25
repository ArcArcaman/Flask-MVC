import mongoengine, json

def read_fields(fields):
    field_return = {}
    possible_fields = ['BinaryField', 'BooleanField', 'ComplexDateTimeField', 'DateTimeField', 'DecimalField', 'DictField', 'DynamicField', 'EmailField', 'EmbeddedDocumentField', 'EmbeddedDocumentListField', 'FileField', 'FloatField', 'GenericReferenceField', 'GenericEmbeddedDocumentField', 'GenericLazyReferenceField', 'GeoPointField', 'ImageField', 'IntField', 'ListField', 'MapField', 'ObjectIdField', 'ReferenceField', 'LazyReferenceField', 'SequenceField', 'SortedListField', 'StringField', 'URLField', 'UUIDField', 'PointField', 'LineStringField', 'PolygonField', 'MultiPointField', 'MultiLineStringField', 'MultiPolygonField']
    for fieldname in fields.keys():
        if field_return.get(fieldname) == None and fields[fieldname].get('field') in possible_fields and fields[fieldname].get('field') != None:
            if fields[fieldname].get('attr') == None: fields[fieldname]['attr'] = ''
            field_return[fieldname] = eval('mongoengine.fields.'+fields[fieldname]['field']+'('+ fields[fieldname]['attr'] +')')
    
    return field_return

class DefineMongo:
    collections = {}

    def __init__(self, connections):
        for connection in connections:
            if connection.get('alias') == None: connection['alias'] = 'default'
            mongoengine.register_connection(**connection)

        # self.collections = {}
        
    @classmethod
    def define_collection(cls, name, fields, db_alias='default', max_documents=None, max_size=None, indexes=None, auto_create_index=True, strict=True): # , temp_connection=None):
        # temp_condition = 0
        # if temp_connection != None:
        #     if temp_connection.get("alias") == None or temp_connection.get("alias") == '' or temp_connection.get("alias") == 'default': assert AttributeError("alias field cannot be empty or default.")
        #     else:
        #         mongoengine.register_connection(**temp_connection)
        #         temp_condition = 1
        if cls.collections.get(name) == None:
            content = read_fields(fields)
            content['meta'] = {}
            meta = content['meta']
            meta['db_alias'] = db_alias
            if max_documents != None: meta['max_documents'] = max_documents
            if max_size != None: meta['max_size'] = max_size
            if indexes != None: meta['indexes'] = indexes
            if auto_create_index != None: meta['auto_create_index'] = auto_create_index
            if strict != None: meta['strict'] = strict
            cls.collections[name] = type(name, (mongoengine.Document,), content)
        # if temp_condition == 1:
        #     mongoengine.connection.disconnect(alias=temp_connection.get("alias"))

    @classmethod
    def add_document(cls, collection_name, **attr):
        if cls.collections.get(collection_name) != None:
            obj = DefineMongo.collections[collection_name](**attr)
            obj.save()
            # if conn_temp == True:
            #     mongoengine.connection.disconnect(alias=self.collections[collection_name].meta.get('db_alias'))
            return {'status': 'SUCCESS'}
        else:
            raise KeyError('Collection ' + collection_name + ' not found.')

def from_json(mongo_json_file, collections_json_file):
    mongo_load = json.load(mongo_json_file)
    if mongo_load.get('connections') == None: raise SyntaxError('connections not found')
    mongo = DefineMongo(mongo_load.get('connections'))

    conn_collections = json.load(collections_json_file)

    for conn_alias in conn_collections.keys():
        for collection in conn_collections[conn_alias]:
            content = collection
            content['db_alias'] = conn_alias
            DefineMongo.define_collection(**content)
    
    return mongo
