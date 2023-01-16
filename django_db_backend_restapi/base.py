import datetime, calendar

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.introspection import BaseDatabaseIntrospection


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
    # compiler_module = "sqlany_django.compiler"
    compiler_module = "django_db_backend_restapi.compiler"

    def quote_name(self, name):
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"{}"'.format(name)

    def adapt_datefield_value(self, value):
        if value is None:
            return None
        return datetime.datetime.utcfromtimestamp(calendar.timegm(value.timetuple()))

    def adapt_datetimefield_value(self, value):
        return value

    def adapt_timefield_value(self, value):
        if value is None:
            return None

        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%H:%M:%S')

        return datetime.datetime(1900, 1, 1, value.hour, value.minute, value.second, value.microsecond)

    def convert_datefield_value(self, value, expression, connection, context):
        if isinstance(value, datetime.datetime):
            value = value.date()
        return value

    def convert_timefield_value(self, value, expression, connection, context):
        if isinstance(value, datetime.datetime):
            value = value.time()
        return value

    def get_db_converters(self, expression):
        converters = super(DatabaseOperations, self).get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == 'DateField':
            converters.append(self.convert_datefield_value)
        elif internal_type == 'TimeField':
            converters.append(self.convert_timefield_value)
        return converters

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        # TODO: Need to implement this fully
        return ['ALTER TABLE']


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'restapi'
    display_name = 'RestAPI'

    SchemaEditorClass = BaseDatabaseSchemaEditor
    Database = Database

    client_class = BaseDatabaseClient
    creation_class = BaseDatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection 
    ops_class = DatabaseOperations

    operators = {
        'exact': '= %s',
        'iexact': 'iLIKE %.*s',
        'contains': 'LIKE %s',
        'icontains': 'iLIKE %s',
        'regex': 'REGEXP BINARY %s',
        'iregex': 'REGEXP %s',
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
        'startswith': 'LIKE %s',
        'endswith': 'LIKE %s',
        'istartswith': 'iLIKE %s',
        'iendswith': 'iLIKE %s',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_usable(self):
        if self.connection is not None:
            return True
        return False

    def get_connection_params(self):
        """
        Default method to acquire database connection parameters.
        Sets connection parameters to match settings.py, and sets
        default values to blank fields.
        """
        valid_settings = {
            'NAME': 'name',
            'URL': 'url',
            'AUTH_TOKEN': 'auth_token',
        }
        connection_params = {
            'name': 'restapi_test',
            'enforce_schema': True
        }
        for setting_name, kwarg in valid_settings.items():
            try:
                setting = self.settings_dict[setting_name]
            except KeyError:
                continue

            if setting or setting is False:
                connection_params[kwarg] = setting

        return connection_params

    def get_new_connection(self, connection_params):
        name = connection_params.pop('name')

        print("CONNECTION")
        print(self.connection)

        return self.connection

    def _set_autocommit(self, autocommit):
        """
        Default method must be overridden, eventhough not used.
        TODO: For future reference, setting two phase commits and rollbacks
        might require populating this method.
        """
        pass

    def init_connection_state(self):
        pass

    def _close(self):
        """
        Closes the client connection to the database.
        """
        # if self.connection:
        #     with self.wrap_database_errors:
        #         self.connection.client.close()
        pass

    def _rollback(self):
        raise NotImplementedError

    def _commit(self):
        """
        Commit routine
        TODO: two phase commits are not supported yet.
        """
        pass
