from django_db_backend_restapi.rest_api_handler import BaseRestApiHandler


class TodoRestApiHandler(BaseRestApiHandler):

    def __init__(self):
        print("!!!! INIT CLASS !!!!")

    def insert(self, query):
        print("--- INSERT ---")
        print(query)

    def get(self, *, model, pk):
        print("---- GET ----")
        print(model)
        print(pk)
        return iter([])
