from django.db.models.fields import AutoFieldMixin, UUIDField, BigIntegerField, AutoFieldMeta

class CustomAutoFieldMeta(AutoFieldMeta):
    @property
    def _subclasses(self):
        return (UUIDAutoField, UUIDAutoField)

class AutoField(AutoFieldMixin, UUIDField, metaclass=CustomAutoFieldMeta):
    def get_internal_type(self):
        return "AutoField"

    def rel_db_type(self, connection):
        return UUIDField().db_type(connection=connection)

class UUIDAutoField(AutoFieldMixin, UUIDField):
    def get_internal_type(self):
        return "UUIDAutoField"

    def rel_db_type(self, connection):
        return UUIDField().db_type(connection=connection)