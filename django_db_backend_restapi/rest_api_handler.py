
class BaseRestApiHandler:

    def list(self):
        raise NotImplementedError

    def get(self, *, model, pk, columns):
        raise NotImplementedError

    def insert(self, query):
        raise NotImplementedError

    def update(self, *, model, pk, values):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
