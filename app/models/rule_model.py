import uuid
from app import db


class FeatureRule(db.Model):
    __tablename__ = "feature_rules"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    feature_id = db.Column(db.String(36), db.ForeignKey("features.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_type = db.Column(db.String(50), nullable=False, index=True)
    rule_value = db.Column(db.String(255), nullable=False)
