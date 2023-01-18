from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class Database(object):
    class Error(Exception):
        pass

    class InterfaceError(Error):
        pass

    class DatabaseError(Error):
        pass

    class DataError(DatabaseError):
        pass

    class OperationalError(DatabaseError):
        pass

    class IntegrityError(DatabaseError):
        pass

    class InternalError(DatabaseError):
        pass

    class ProgrammingError(DatabaseError):
        pass

    class NotSupportedError(DatabaseError):
        pass


class DatabaseIntrospection(BaseDatabaseIntrospection):
    pass


class DatabaseFeatures(BaseDatabaseFeatures):
    atomic_transactions = False
    allows_group_by_pk = False
    empty_fetchmany_value = []
    has_bulk_insert = False
    has_select_for_update = False
    has_zoneinfo_database = False
    related_fields_match_type = False
    supports_regex_backreferencing = False
    supports_sequence_reset = False
    update_can_self_select = False
    uses_custom_query_class = False


class DatabaseOperations(BaseDatabaseOperations):
    compiler_module = "django_restapi_engine.compiler"

    def quote_name(self, name):
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"{}"'.format(name)


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = "restapi"
    display_name = "RestAPI"

    SchemaEditorClass = BaseDatabaseSchemaEditor
    Database = Database

    client_class = BaseDatabaseClient
    creation_class = BaseDatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations

    def get_connection_params(self):
        pass

    def get_new_connection(self, connection_params):
        pass

    def init_connection_state(self):
        pass

    def create_cursor(self, name=None):
        raise NotImplementedError("RestAPI Engine does not support cursor")
