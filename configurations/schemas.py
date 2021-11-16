from mkondo import marshmallow
from .models import Configuration

class ConfigurationSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = Configuration
        fields = ('key', 'value', 'configuration_id')
        dump_only = ('configuration_id',)