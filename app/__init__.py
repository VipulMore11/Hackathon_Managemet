from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
