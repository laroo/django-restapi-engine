import pytest  # type: ignore

from django_restapi_engine.rest_api_handler import BaseRestApiHandler


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
