from app.models import Feature
import hashlib
from app import cache

@cache.memoize(timeout=60) 
def is_feature_enabled_for_user(feature_name: str, user_id: str) -> bool:
    feature = Feature.query.filter_by(name=feature_name).first()
    if not feature or not feature.is_enabled:
        return False

    for rule in feature.rules:
        if rule.rule_type == "user_id" and str(user_id) == str(rule.rule_value):
            return True
        if rule.rule_type == "percentage":
            percentage = int(rule.rule_value)
            hash_value = int(hashlib.sha256(str(user_id).encode()).hexdigest(), 16)
            if hash_value % 100 < percentage:
                return True

    return False