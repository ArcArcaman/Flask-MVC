from connector.definemongo import *
from types import FunctionType
try:
    from mongoengine.queryset import Q, QCombination
except:
    from mongoengine.queryset.visitor import Q, QCombination

class hide_meta(type):
    def __new__(cls, cls_name, cls_bases, cls_dict):
        cls_dict.setdefault("__excluded__", [])
        out_cls = super(hide_meta, cls).__new__(cls, cls_name, cls_bases, cls_dict)

        def __getattribute__(self, name):
            if name in cls_dict["__excluded__"]:
                raise AttributeError(name)
            else:
                return super(out_cls, self).__getattribute__(name)
        out_cls.__getattribute__ = __getattribute__

        def __dir__(self):
            return sorted((set(dir(out_cls)) | set(self.__dict__.keys())) - set(cls_dict["__excluded__"])) 
        out_cls.__dir__ = __dir__

        return out_cls

class BasicDMDocument:
    def __init__(self, collection):
        self.collection = collection

    def query(self, command='fetch', **fields):
        queries = list(set([x for x, y in self.__class__.__dict__.items() if type(y) == FunctionType and not x.startswith("__")] + [x for x, y in BasicDMDocument.__dict__.items() if type(y) == FunctionType and not x.startswith("__")]))

        if command in queries:
            return getattr(self, command)(**fields)

    def append(self, **fields):
        if DefineMongo.add_document(self.collection, **fields).get('status') == 'SUCCESS':
            return 'Data Append Successful.'

    def remove(self, **filters):
        return DefineMongo.collections[self.collection].objects(**filters).delete()

    def fetch(self, **filters):
        if(len(filters.keys()) > 1):
            queries = map(lambda i: Q(**{i[0]: i[1]}), filters.items())
            query = QCombination(QCombination.AND, queries)
            return DefineMongo.collections[self.collection].objects(query).as_pymongo()
        else:
            return DefineMongo.collections[self.collection].objects(**filters).as_pymongo()

    def fetchOrder(self, **filters):
        if(filters.get("$__order__") == None):
            return self.fetch(**filters)
        else:
            order = filters.pop("$__order__", None)
            temp_limit = filters.pop("$__limit__", None)
            queries = map(lambda i: Q(**{i[0]: i[1]}), filters.items())
            query = QCombination(QCombination.AND, queries)
            if(temp_limit == None): return DefineMongo.collections[self.collection].objects(query).order_by(*order).as_pymongo()
            else: return DefineMongo.collections[self.collection].objects(query).limit(int(temp_limit)).order_by(*order).as_pymongo()
    
