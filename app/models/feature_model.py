import uuid
from datetime import datetime
from app import db

class Feature(db.Model):
    __tablename__ = "features"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    is_enabled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    rules = db.relationship("FeatureRule", backref="feature", cascade="all, delete-orphan", lazy=True)
