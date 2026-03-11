from flask import Blueprint, request, jsonify
from app.models import Feature
from app.schemas.feature_schema import FeatureSchema
from app.services.feature_service import is_feature_enabled_for_user
from app import db

features_bp = Blueprint("features", __name__, url_prefix="/features")

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

@features_bp.route("", methods=["POST"])
def create_feature():
    json_data = request.get_json()
    data = feature_schema.load(json_data)
    feature = Feature(**data)
    db.session.add(feature)
    db.session.commit()
    return feature_schema.dump(feature), 201

@features_bp.route("", methods=["GET"])
def get_features():
    features = Feature.query.all()
    return features_schema.dump(features)

@features_bp.route("/<string:feature_id>", methods=["PATCH"])
def update_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    data = feature_schema.load(request.get_json(), partial=True)
    for key, value in data.items():
        setattr(feature, key, value)

    db.session.commit()
    return feature_schema.dump(feature)

@features_bp.route("/check", methods=["GET"])
def check_feature():
    feature_name = request.args.get("feature")
    user_id = request.args.get("user_id")
    enabled = is_feature_enabled_for_user(feature_name, user_id)
    return jsonify({
        "feature": feature_name,
        "user_id": user_id,
        "enabled": enabled
    })