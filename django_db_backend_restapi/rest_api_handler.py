
class BaseRestApiHandler:

    def list(self):
        raise NotImplementedError

    def get(self, *, model, pk):
        raise NotImplementedError

    def insert(self, query):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

