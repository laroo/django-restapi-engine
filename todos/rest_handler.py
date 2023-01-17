from typing import Optional
from django_db_backend_restapi.rest_api_handler import BaseRestApiHandler
from django.db.models.aggregates import Count
import requests


class TodoRestApiHandler(BaseRestApiHandler):

    COLUMN_MAPPING = {'user_id': 'userId'}  # Model -> API

    def insert(self, *, model, obj, fields, returning_fields):

        data = {}
        for field in fields:
            data[self.COLUMN_MAPPING.get(field.name, field.name)] = getattr(obj, field.name)

        r = requests.post(f"https://jsonplaceholder.typicode.com/todos", json=data)
        if r.status_code == 201:
            row = r.json()

            output = []
            for field in returning_fields:
                output.append(row[self.COLUMN_MAPPING.get(field.name, field.name)])

            return output

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

    def delete(self, *, model, pk):
        r = requests.delete(f"https://jsonplaceholder.typicode.com/todos/{pk}")
        if r.status_code == 200:
            return

    def list(self, *, model, columns, query):
        """
        columns:
        [
            (Col(todos_todo, todos.Todo.id), ('"todos_todo"."id"', []), None),
            (Col(todos_todo, todos.Todo.user_id), ('"todos_todo"."user_id"', []), None),
            (Col(todos_todo, todos.Todo.title), ('"todos_todo"."title"', []), None),
            (Col(todos_todo, todos.Todo.completed), ('"todos_todo"."completed"', []), None)
        ]
        """
        r = requests.get(f"https://jsonplaceholder.typicode.com/todos?_limit=8")
        if r.status_code == 200:
            rows = r.json()

        if len(columns) == 1 and isinstance(columns[0][0], Count):
            return len(rows)

        output = []
        for row in rows:
            row_output = []
            for col, _, _ in columns:
                row_output.append(row[self.COLUMN_MAPPING.get(col.target.name, col.target.name)])
            output.append(row_output)

        return output
