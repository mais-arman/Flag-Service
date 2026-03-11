from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Feature, FeatureRule

    from app.routes.features import features_bp
    from app.routes.rules import rules_bp

    app.register_blueprint(features_bp)
    app.register_blueprint(rules_bp)

    return app