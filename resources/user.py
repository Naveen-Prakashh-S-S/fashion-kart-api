from db import db
from models import UserModel
from schemas import UserSchema, UserLoginSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token
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
        
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"] or UserModel.email == user_data["username"]
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id) , fresh=True)
            refresh_token = create_refresh_token(identity= str(user.id) )
            return {"access_token": access_token, "refresh token":refresh_token}
        abort(401, message="Invalid UserName and Password..")     
        