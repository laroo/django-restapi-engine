from typing import Optional
from django_db_backend_restapi.rest_api_handler import BaseRestApiHandler
import requests


class TodoRestApiHandler(BaseRestApiHandler):

    COLUMN_MAPPING = {'user_id': 'userId'}  # Model -> API

    def insert(self, *, model, values):
        print("--- INSERT ---")
        print(model)
        print(values)

    def get(self, *, model, pk, columns):
        """

        columns:
        [
            (Col(todos_todo, todos.Todo.id), ('"todos_todo"."id"', []), None),
            (Col(todos_todo, todos.Todo.user_id), ('"todos_todo"."user_id"', []), None),
            (Col(todos_todo, todos.Todo.title), ('"todos_todo"."title"', []), None),
            (Col(todos_todo, todos.Todo.completed), ('"todos_todo"."completed"', []), None)
        ]
        """
        r = requests.get(f"https://jsonplaceholder.typicode.com/todos/{pk}")
        if r.status_code == 200:
            row = r.json()

        output = []
        for col, _, _ in columns:
            output.append(row[self.COLUMN_MAPPING.get(col.target.name, col.target.name)])

        return output


    def update(self, *, model, pk, values) -> Optional[int]:
        """
        Values is a list of tuples that identify (column, model, value)

        Return num rows changed
        """
        data = {}
        for col, model, value in values:
            data[self.COLUMN_MAPPING.get(col.name, col.name)] = value

        r = requests.put(f"https://jsonplaceholder.typicode.com/todos/{pk}", json=data)
        if r.status_code == 200:
            return 1

        return 0
