import re
import typing
from logging import getLogger

from sqlparse import parse as sqlparse
from sqlparse import tokens
from sqlparse.sql import (
    IdentifierList, Identifier, Parenthesis,
    Where, Token,
    Statement)


logger = getLogger(__name__)


class Result:

    def __init__(self,
                 connection,
                 # client_connection, #: MongoClient,
                 # db_connection, #: Database,
                 # connection_properties, #: 'base.DjongoClient',
                 sql: str,
                 params: typing.Optional[list]):
        print("---- Result::__init__ ----")

        self._params = params
        # self.db = db_connection
        self.connection = connection
        # self.cli_con = client_connection
        # self.connection_properties = connection_properties
        self._params_index_count = -1
        self._sql = re.sub(r'%s', self._param_index, sql)
        self.last_row_id = None
        self._result_generator = None

        self._query = None
        self.parse()

    def count(self):
        print("COUNT")
        return self._query.count()

    def close(self):
        if self._query and self._query._cursor:
            self._query._cursor.close()

    def __next__(self):
        if self._result_generator is None:
            self._result_generator = iter(self)

        return next(self._result_generator)

    next = __next__

    def __iter__(self):
        print("---- Result::__iter__ ----")
        # yield dict(id=1, user_id=2, title="Testing123", completed=False)
        # yield (("id", "user_id", "title", "completed"), (1,2,"Testing123", False))
        yield (1, 2, "Testing123", False)
        # yield (2, 3, "Testing123", True)
        return None

        print("self._query", self._query)
        if self._query is None:
            return None

        yield from iter(self._query)
        # try:
        #     yield from iter(self._query)
        #
        # except MigrationError:
        #     raise
        #
        # except OperationFailure as e:
        #     import djongo
        #     exe = SQLDecodeError(
        #         f'FAILED SQL: {self._sql}\n'
        #         f'Pymongo error: {e.details}\n'
        #         f'Version: {djongo.__version__}'
        #     )
        #     raise exe from e
        #
        # except Exception as e:
        #     import djongo
        #     exe = SQLDecodeError(
        #         f'FAILED SQL: {self._sql}\n'
        #         f'Version: {djongo.__version__}'
        #     )
        #     raise exe from e

    def _param_index(self, _):
        self._params_index_count += 1
        return '%({})s'.format(self._params_index_count)

    def parse(self):
        print("---- Result::parse ----")
        print("self.connection", type(self.connection))
        print(self._sql)
        logger.info(f'\n sql_command: {self._sql}')
        statement = sqlparse(self._sql)

        # if len(statement) > 1:
        #     raise SQLDecodeError(self._sql)

        statement = statement[0]
        sm_type = statement.get_type()
        print("statement", type(statement))
        print("sm_type", sm_type)



class Cursor:

    def __init__(self,
                 connection,
                 ):
        self.connection = connection
        # self.client_conn = client_conn
        # self.connection_properties = connection_properties
        self.result = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.result is not None:
            self.result.close()

    def __getattr__(self, name):
        print(f"---- Cursus::__getattr__(name={name}) ----")
        # try:
        #     return getattr(self.result, name)
        # except AttributeError:
        #     pass
        #
        # try:
        #     return getattr(self.db_conn, name)
        # except AttributeError:
        #     raise

    @property
    def rowcount(self):
        if self.result is None:
            raise RuntimeError

        return self.result.count()

    @property
    def lastrowid(self):
        return self.result.last_row_id

    def execute(self, sql, params=None):
        self.result = Result(self.connection, sql, params)

    def fetchmany(self, size=1):
        ret = []
        for _ in range(size):
            try:
                ret.append(self.result.next())
            except StopIteration:
                break

        return ret

    def fetchone(self):
        try:
            return self.result.next()
        except StopIteration:
            return []

    def fetchall(self):
        return list(self.result)

