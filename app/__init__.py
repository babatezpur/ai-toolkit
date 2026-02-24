from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import models so Flask-Migrate can detect them
    from app.models import User, SavedItem, SearchedItem

    # Register blueprints (import here to avoid circular imports)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.facts import facts_bp
    app.register_blueprint(facts_bp)
    from app.routes.quotes import quotes_bp
    app.register_blueprint(quotes_bp)
    from app.routes.conversation import conversation_bp
    app.register_blueprint(conversation_bp)

    return app