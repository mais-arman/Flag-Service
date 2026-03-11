import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    strategy="fixed-window"
)

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    from app.models import Feature, FeatureRule

    from app.routes.features import features_bp
    from app.routes.rules import rules_bp

    app.register_blueprint(features_bp)
    app.register_blueprint(rules_bp)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app