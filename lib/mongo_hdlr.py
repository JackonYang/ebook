# -*- coding: utf-8 -*-
#!/usr/bin/python
import pymongo


class MongodbHandler():
    def __init__(self):
        self.db = False

    def __del__(self):
        self.disconnect()

    def connect(self, host, port):
        try:
            self.db = pymongo.Connection(host, int(port))
        except:
            return False
        else:
            return self.check_connect()

    def disconnect(self):
        if self.check_connect():
            self.db.disconnect()
            self.db = False

    def check_connect(self):
        if isinstance(self.db, pymongo.connection.Connection):
            return True
        else:
            return False

    def get_dbs(self):
        if self.check_connect():
            return self.db.database_names()

    def get_collections(self, database):
        if self.check_connect():
            return self.db[database].collection_names()

    def GetDocuments(self, database, collection, **kwargs):
        """Returns documents from database and collection params

        May receive the following kwargs:
        - find = Dict for querying the collection
        - fields = Dict containing the fields that will return
        - page = Int for skipping documents (starts with ZERO)
        - limit = Int for maximum documents returned

        """
        # para settings
        page = kwargs.get('page', 0)
        limit = kwargs.get('limit', 10)

        # para check
        page = max(page, 0)

        query = self.db[database][collection].find(kwargs.get('find', {}), fields=kwargs.get('fields', None)).skip(page * limit).limit(limit)

        return {'err': False, 'result': query}

    def CountDocuments(self, database, collection, **kwargs):
        return self.db[database][collection].find(kwargs.get('find', {}), fields=kwargs.get('fields', None)).count()

    def UpdateDocuments(self, database, collection, **kwargs):
        """Updates documents from database and collection params

        May receive the following kwargs:
        - find = Dict for filtering the update
        - update = Dict containing the update object
        - multi = Bool for multi flag
        - upsert = Bool for upsert flag

        """
        result = self.db[database][collection].update(kwargs.get('find', {}), kwargs.get('update', {}), multi=kwargs.get('multi', False), upsert=kwargs.get('upsert', False), safe=True)
        if result['err']:
            return {'err': True}
        else:
            return {'err': False, 'affected': result['n']}

    def RunAggregation(self, database, collection, pipeline_param, **kwargs):
        if isinstance(pipeline_param, list):
            try:
                res = self.db[database].command('aggregate', collection, pipeline=pipeline_param)
            except pymongo.errors.OperationFailure as e:
                return {'err': True, 'errmsg': e.message}
            except:
                return {'err': True, 'errmsg': 'Error on operation'}
            else:
                return {'err': False, 'result': res['result']}
        else:
            return False
