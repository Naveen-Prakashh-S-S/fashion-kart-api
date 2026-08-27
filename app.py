from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
 
 
db = SQLAlchemy()

migrate = Migrate()
 
 
def create_app():
    app = Flask(__name__)
 
    app.config["API_TITLE"] = "Dress Shopping API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dress_shop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 
    db.init_app(app)
    migrate.init_app(app, db)
 
    api = Api(app)
 
    return app
