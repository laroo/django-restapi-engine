import collections
import pdb
import re
from functools import partial
from itertools import chain

from django.core.exceptions import EmptyResultSet, FieldError
from django.db import DatabaseError, NotSupportedError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import F, OrderBy, RawSQL, Ref, Value
from django.db.models.functions import Cast, Random
from django.db.models.query_utils import Q, select_related_descend
from django.db.models.sql.constants import (
    CURSOR, GET_ITERATOR_CHUNK_SIZE, MULTI, NO_RESULTS, ORDER_DIR, SINGLE,
)
from django.db.models.sql.query import Query, get_order_dir
from django.db.transaction import TransactionManagementError
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.utils.regex_helper import _lazy_re_compile


from django.db.models.sql.query import Query
from django.db.models.sql.subqueries import UpdateQuery

from django.utils.module_loading import import_string
from .rest_api_handler import BaseRestApiHandler

from django.db.models.sql.compiler import SQLCompiler as DefaultSQLCompiler
from django.db.models.sql.compiler import SQLUpdateCompiler as DefaultSQLUpdateCompiler
from django.db.models.sql.compiler import SQLInsertCompiler as DefaultSQLInsertCompiler
from django.db.models.sql.compiler import SQLDeleteCompiler as DefaultSQLDeleteCompiler

from django.db.models.expressions import Col
from django.db.models.lookups import Exact, In

from django.db.models.sql.subqueries import UpdateQuery, InsertQuery, DeleteQuery


class RestApiCompilerMixin:

    def __init__(self,
                 query: "django.db.models.sql.query.Query",
                 connection: "django_db_backend_restapi.base.DatabaseWrapper",
                 using: str
                 ):
        super().__init__(query, connection, using)

        default_handler_class = self.connection.settings_dict['DEFAULT_HANDLER_CLASS']
        handler_class = import_string(default_handler_class)
        self.handler: BaseRestApiHandler = handler_class()


class SQLCompiler(RestApiCompilerMixin, DefaultSQLCompiler):


    def execute_sql(self, result_type=MULTI, chunked_fetch=False, chunk_size=GET_ITERATOR_CHUNK_SIZE):
        """
        Run the query against the database and return the result(s). The
        return value is a single data item if result_type is SINGLE, or an
        iterator over the results if the result_type is MULTI.

        result_type is either MULTI (use fetchmany() to retrieve all rows),
        SINGLE (only retrieve a single row), or None. In this last case, the
        cursor is returned if any query is executed, since it's used by
        subclasses such as InsertQuery). It's possible, however, that no query
        is needed, as the filters describe an empty set. In that case, None is
        returned, to avoid any unnecessary database interaction.
        """
        self.pre_sql_setup()

        model = self.query.model
        model_pk_field = model._meta.pk

        single_where_node = self.query.where.children[0] if self.query.where and len(self.query.where.children) == 1 else None

        if isinstance(single_where_node, Exact) and single_where_node.lhs.target == model_pk_field:
            row = self.handler.get(model=model, pk=single_where_node.rhs, columns=self.select)
            return iter([[row]])

        rows = self.handler.list(model=model, columns=self.select, query=self.query)
        return iter([rows])


class SQLInsertCompiler(RestApiCompilerMixin, DefaultSQLInsertCompiler):

    def execute_sql(self, returning_fields=None):
        self.pre_sql_setup()
        self.query: InsertQuery

        model = self.query.model

        assert len(self.query.objs) == 1

        row = self.handler.insert(model=model, obj=self.query.objs[0], fields=self.query.fields, returning_fields=returning_fields)
        return [row]


class SQLDeleteCompiler(RestApiCompilerMixin, DefaultSQLDeleteCompiler):

    def execute_sql(self, result_type=MULTI, chunked_fetch=False, chunk_size=GET_ITERATOR_CHUNK_SIZE):
        self.pre_sql_setup()
        self.query: DeleteQuery

        model = self.query.model
        model_pk_field = model._meta.pk

        single_where_node = self.query.where.children[0] if self.query.where and len(self.query.where.children) == 1 else None

        if isinstance(single_where_node, Exact) and single_where_node.lhs.target == model_pk_field:
            self.handler.delete(model=model, pk=single_where_node.rhs)
        elif isinstance(single_where_node, In) and single_where_node.lhs.target == model_pk_field:
            for pk in single_where_node.rhs:
                self.handler.delete(model=model, pk=pk)


class SQLUpdateCompiler(RestApiCompilerMixin, DefaultSQLUpdateCompiler):

    def execute_sql(self, result_type):
        self.pre_sql_setup()
        self.query: UpdateQuery

        model = self.query.model
        model_pk_field = model._meta.pk

        single_where_node = self.query.where.children[0] if self.query.where and len(self.query.where.children) == 1 else None

        if isinstance(single_where_node, Exact) and single_where_node.lhs.target == model_pk_field:
            num_rows_updated = self.handler.update(model=model, pk=single_where_node.rhs, values=self.query.values)
            return num_rows_updated
        raise NotImplementedError("Unsupported UPDATE")


class SQLAggregateCompiler(RestApiCompilerMixin, DefaultSQLCompiler):
    pass
