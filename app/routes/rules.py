from flask import Blueprint, request, jsonify
from app.models import Feature, FeatureRule
from app.schemas.rule_schema import FeatureRuleSchema
from app import db

rules_bp = Blueprint("rules", __name__)

rule_schema = FeatureRuleSchema()


@rules_bp.route("/features/<string:feature_id>/rules", methods=["POST"])
def create_rule(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    data = rule_schema.load(request.json)
    rule_type = data["rule_type"]
    rule_value = data["rule_value"]
    if rule_type == "percentage":
        try:
            percentage = int(rule_value)
        except ValueError:
            return jsonify({"error": "percentage must be integer"}), 400
        
        if percentage < 0 or percentage > 100:
            return jsonify({
                "error": "percentage must be between 0 and 100"
            }), 400
    rule = FeatureRule(feature_id=feature.id, **data)
    db.session.add(rule)
    db.session.commit()
    return rule_schema.dump(rule), 201