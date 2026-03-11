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
    if not json_data:  
        return jsonify({"error": "Invalid request body"}), 400
    data = feature_schema.load(json_data)    
    feature = Feature(**data)
    db.session.add(feature)
    db.session.commit()
    return feature_schema.dump(feature), 201

@features_bp.route("", methods=["GET"])
def get_features():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)
    pagination = Feature.query.paginate(page=page, per_page=limit, error_out=False)
    features = pagination.items
    return jsonify({
        "data": features_schema.dump(features),
        "pagination": {
            "page": page,
            "limit": limit,
            "total": pagination.total,
            "pages": pagination.pages
        }
    })    

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

    if not feature_name or not user_id:
        return jsonify({
            "error": "feature and user_id are required"
        }), 400

    enabled = is_feature_enabled_for_user(feature_name, user_id)
    return jsonify({
        "feature": feature_name,
        "user_id": user_id,
        "enabled": enabled
    })