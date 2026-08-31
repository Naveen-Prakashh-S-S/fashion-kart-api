from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import models 
# Import to Use the Blueprint to Register Line no: 29
from resources import TagsBlueprint
from db import db



 
 
def create_app():
    app = Flask(__name__)
 
    app.config["API_TITLE"] = "Dress Shopping API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dress_shop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
 
    api = Api(app)
    api.register_blueprint(TagsBlueprint)
    return app
