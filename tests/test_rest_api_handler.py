import pytest  # type: ignore
from django.db import models

from django_restapi_engine.rest_api_handler import BaseRestApiHandler


class Todo(models.Model):
    id = models.AutoField(primary_key=True)  # type: ignore
    title = models.CharField(max_length=200)  # type: ignore
    completed = models.BooleanField(default=True)  # type: ignore

    class Meta:
        managed = False


def test_api_handler_class__list_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseRestApiHandler().list(model=None, columns=None, query=None)

    with pytest.raises(NotImplementedError):
        BaseRestApiHandler().get(model=None, pk=None, columns=None)

    with pytest.raises(NotImplementedError):
        BaseRestApiHandler().insert(model=None, obj=None, fields=None, returning_fields=None)

    with pytest.raises(NotImplementedError):
        BaseRestApiHandler().update(model=None, pk=None, values=None)

    with pytest.raises(NotImplementedError):
        BaseRestApiHandler().delete(model=None, pk=None)


def test_list():
    Todo.objects.using("restapi")
