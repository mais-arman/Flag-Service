from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import Feature
from app import db

class FeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = False
        sqla_session = db.session 
        

    id = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)    