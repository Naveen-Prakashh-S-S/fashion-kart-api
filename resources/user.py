from db import db
from models import UserModel
from schemas import UserSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

blp = Blueprint("Users", "user", description = "User Endpoint Operations")

@blp.route("/user/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        data = UserModel.query.filter_by(username=user_data["username"]).first()
        if (data):
            abort(400, message = "User Name Already Exists...")
        data = UserModel.query.filter_by(email=user_data["email"]).first()
        if (data):
            abort(400, message = "Email Already Exists...")

        user = UserModel(username = user_data["username"], email = user_data["email"] ,password = pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()

        return {"Message": "User Registered Successfully"}, 201
        
        
        