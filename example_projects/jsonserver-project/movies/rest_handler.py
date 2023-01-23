import json
from typing import Optional
from urllib.parse import urlencode

import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.aggregates import Count

from django_restapi_engine.rest_api_handler import BaseRestApiHandler


class MovieCollectionApiHandler(BaseRestApiHandler):

    BASE_URL = "http://localhost:3000"

    def get_api_endpoint(self, model, pk=None):
        """
        Build API endpoint url based on model's `db_table`
        """
        if pk:
            return f"{self.BASE_URL}/{model._meta.db_table}/{pk}"
        return f"{self.BASE_URL}/{model._meta.db_table}"

    def insert(self, *, model, obj, fields, returning_fields):

        data = {}
        for field in fields:
            data[field.name] = getattr(obj, field.name)

        r = requests.post(
            self.get_api_endpoint(model),
            data=json.dumps(data, cls=DjangoJSONEncoder),
            headers={"content-type": "application/json"},
        )
        if r.status_code != 201:
            raise ValueError("Unexpected response status code %s when inserting record", r.status_code)

        row = r.json()

        output = []
        for field in returning_fields:
            output.append(row[field.name])

        return output

    def get(self, *, model, pk, columns):
        r = requests.get(self.get_api_endpoint(model, pk))
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when fetching record", r.status_code)

        row = r.json()
        output = []
        for col, _, _ in columns:
            output.append(row[col.target.name])

        return output

    def update(self, *, model, pk, values) -> Optional[int]:
        data = {}
        for col, _, value in values:
            data[col.name] = value

        r = requests.put(
            self.get_api_endpoint(model, pk),
            data=json.dumps(data, cls=DjangoJSONEncoder),
            headers={"content-type": "application/json"},
        )
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when updating record", r.status_code)

        return 1

    def delete(self, *, model, pk):
        r = requests.delete(self.get_api_endpoint(model, pk))
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when deleting record", r.status_code)

    def list(self, *, model, columns, query):
        """
        Supported API features: https://github.com/typicode/json-server
        """
        if len(columns) == 1 and isinstance(columns[0][0], Count):
            # Count
            r = requests.get(self.get_api_endpoint(model))
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
                api_column = sort_column.lstrip("-")
                sort[api_column] = "desc" if sort_column[:1] == "-" else "asc"

            params = {
                "_sort": ",".join(sort.keys()),
                "_order": ",".join(sort.values()),
                "_start": query.low_mark,
                "_end": query.high_mark,
            }
            clean_params = {k: v for k, v in params.items() if v}  # Remove empty params
            return f"{self.get_api_endpoint(model)}?{urlencode(clean_params)}"

        r = requests.get(build_fetch_url())
        if r.status_code != 200:
            raise ValueError("Unexpected response status code %s when listing records", r.status_code)

        rows = r.json()
        output = []
        for row in rows:
            row_output = []
            for col, _, _ in columns:
                row_output.append(row[col.target.name])
            output.append(row_output)

        return output
