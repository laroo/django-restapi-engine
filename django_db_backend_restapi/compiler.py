import collections
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


class SQLBaseCompiler:

    def __init__(self,
                 query: "django.db.models.sql.query.Query",
                 connection: "django_db_backend_restapi.base.DatabaseWrapper",
                 using: str
                 ):
        print("CUSTOM COMPILER")
        print(self.__class__.__name__)

        self.query = query
        self.connection = connection
        self.using = using

        default_handler_class = self.connection.settings_dict['DEFAULT_HANDLER_CLASS']
        handler_class = import_string(default_handler_class)
        self.handler: BaseRestApiHandler = handler_class()


class SQLCompiler(SQLBaseCompiler):

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
        model = self.query.model
        model_pk_field = model._meta.pk

        from django.db.models.expressions import Col
        from django.db.models.lookups import Exact
        single_where_node = self.query.where.children[0] if self.query.where and len(self.query.where.children) == 1 else None

        if isinstance(single_where_node, Exact) and single_where_node.lhs.target == model_pk_field:
            print("GET ID")
            print(single_where_node.rhs)
            return self.handler.get(model=model, pk=single_where_node.rhs)

        return

        import pdb; pdb.set_trace()

        result_type = result_type or NO_RESULTS
        try:
            # sql, params = self.as_sql()
            sql = "DUMMY"
            params = {}
            if not sql:
                raise EmptyResultSet
        except EmptyResultSet:
            if result_type == MULTI:
                return iter([])
            else:
                return
        if chunked_fetch:
            cursor = self.connection.chunked_cursor()
        else:
            cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
        except Exception:
            # Might fail for server-side cursors (e.g. connection closed)
            cursor.close()
            raise

        if result_type == CURSOR:
            # Give the caller the cursor to process and close.
            return cursor
        if result_type == SINGLE:
            try:
                val = cursor.fetchone()
                if val:
                    return val[0:self.col_count]
                return val
            finally:
                # done with the cursor
                cursor.close()
        if result_type == NO_RESULTS:
            cursor.close()
            return

        result = cursor_iter(
            cursor, self.connection.features.empty_fetchmany_value,
            self.col_count if self.has_extra_select else None,
            chunk_size,
        )
        if not chunked_fetch or not self.connection.features.can_use_chunked_reads:
            try:
                # If we are using non-chunked reads, we return the same data
                # structure as normally, but ensure it is all read into memory
                # before going any further. Use chunked_fetch if requested,
                # unless the database doesn't support it.
                return list(result)
            finally:
                # done with the cursor
                cursor.close()
        return result


class SQLInsertCompiler(SQLBaseCompiler):

    def execute_sql(self, returning_fields=None):
        self.handler.insert(self.query)
        return []


class SQLDeleteCompiler(SQLBaseCompiler):

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
        pass


class SQLUpdateCompiler(SQLBaseCompiler):

    def execute_sql(self, result_type):
        return 1


class SQLAggregateCompiler(SQLBaseCompiler):
    pass


def cursor_iter(cursor, sentinel, col_count, itersize):
    """
    Yield blocks of rows from a cursor and ensure the cursor is closed when
    done.
    """
    try:
        for rows in iter((lambda: cursor.fetchmany(itersize)), sentinel):
            yield rows if col_count is None else [r[:col_count] for r in rows]
    finally:
        cursor.close()
