from typing import Optional
from urllib.parse import urlencode

import requests
from django.db.models.aggregates import Count

from django_restapi_engine.rest_api_handler import BaseRestApiHandler


class TodoRestApiHandler(BaseRestApiHandler):

    COLUMN_MAPPING = {"pk": "id", "user_id": "userId"}  # Model -> API

    def insert(self, *, model, obj, fields, returning_fields):

        data = {}
        for field in fields:
            data[self.COLUMN_MAPPING.get(field.name, field.name)] = getattr(obj, field.name)

        r = requests.post("https://jsonplaceholder.typicode.com/todos", json=data)
        if r.status_code != 201:
            raise ValueError("Unexpected response status code %s when inserting record", r.status_code)

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
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when fetching record", r.status_code)

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
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when updating record", r.status_code)

        return 1

    def delete(self, *, model, pk):
        r = requests.delete(f"https://jsonplaceholder.typicode.com/todos/{pk}")
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when deleting record", r.status_code)

    def list(self, *, model, columns, query):
        """
        Supported API features: https://github.com/typicode/json-server

        columns:
        [
            (Col(todos_todo, todos.Todo.id), ('"todos_todo"."id"', []), None),
            (Col(todos_todo, todos.Todo.user_id), ('"todos_todo"."user_id"', []), None),
            (Col(todos_todo, todos.Todo.title), ('"todos_todo"."title"', []), None),
            (Col(todos_todo, todos.Todo.completed), ('"todos_todo"."completed"', []), None)
        ]
        """
        if len(columns) == 1 and isinstance(columns[0][0], Count):
            # Count
            r = requests.get("https://jsonplaceholder.typicode.com/todos")
            if r.status_code != 200:
                raise ValueError("Unexpected response status code %s when counting records", r.status_code)
            return len(r.json())

        def build_fetch_url():
            """
            Extract ordering and offset/limit from query and convert it to RestAPI params
            """
            sort = {}
            for sort_column in query.order_by:
                # Django prepends a minus (-) to a sorting column to indicate it's reverse ordering
                api_column = self.COLUMN_MAPPING.get(sort_column.lstrip("-"), sort_column.lstrip("-"))
                sort[api_column] = "desc" if sort_column[:1] == "-" else "asc"

            params = {
                "_sort": ",".join(sort.keys()),
                "_order": ",".join(sort.values()),
                "_start": query.low_mark,
                "_end": query.high_mark,
            }
            clean_params = {k: v for k, v in params.items() if v}  # Remove empty params
            return f"https://jsonplaceholder.typicode.com/todos?{urlencode(clean_params)}"

        r = requests.get(build_fetch_url())
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when listing records", r.status_code)

        rows = r.json()
        output = []
        for row in rows:
            row_output = []
            for col, _, _ in columns:
                row_output.append(row[self.COLUMN_MAPPING.get(col.target.name, col.target.name)])
            output.append(row_output)

        return output
