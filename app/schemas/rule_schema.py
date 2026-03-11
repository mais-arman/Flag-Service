from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import FeatureRule

class FeatureRuleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FeatureRule

    id = auto_field(dump_only=True)
    rule_type = auto_field(required=True)
    rule_value = auto_field(required=True)