
class BaseRestApiHandler:

    def list(self, *, model, columns, query):
        raise NotImplementedError

    def get(self, *, model, pk, columns):
        raise NotImplementedError

    def insert(self, *, model, obj, fields, returning_fields):
        raise NotImplementedError

    def update(self, *, model, pk, values):
        raise NotImplementedError

    def delete(self, *, model, pk):
        raise NotImplementedError
