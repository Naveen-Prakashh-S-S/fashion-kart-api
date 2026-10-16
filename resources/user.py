from db import db
from models import UserModel, ProductModel, TagsModel, CartModel
from schemas import UserSchema, UserLoginSchema,UserProfileSchema, ProductSchema, TagSchema, PlainProductSchema, CartSchema
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

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
        
@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if not user:
            user = UserModel.query.filter(
                        UserModel.email == user_data["username"]
                    ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id) , fresh=True)
            refresh_token = create_refresh_token(identity= str(user.id) )
            return {"access_token": access_token, "refresh token":refresh_token}
        abort(401, message="Invalid UserName and Password..")   

@blp.route("/user/profile")
class UserProfile(MethodView):
    @jwt_required()
    @blp.response(200,UserProfileSchema)
    def get(self):
        jwt = get_jwt_identity()
        user = UserModel.query.get(int(jwt))
        if not user :
            abort (404, message = "User not found")
        return user 

@blp.route("/product")
class BrowseProduct(MethodView):
    @blp.response(200, ProductSchema(many = True))
    def get(self):
        return ProductModel.query.all()

@blp.route("/product/<int:product_id>")
class SearchProduct(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        return ProductModel.query.get_or_404(product_id)

@blp.route("/tags/<int:tag_id>/products")
class SearchTagProduct(MethodView):
    @blp.response(200, PlainProductSchema(many = True))
    def get(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag.products

@blp.route("/products/search")
class SearchByName(MethodView):
    @blp.response(200, PlainProductSchema(many = True))
    def get(self):
        name = request.args.get("name", "").strip()
        products = ProductModel.query.filter( ProductModel.name.ilike(f"%{name}%")).all()
        return products

@blp.route("/cart")
class CartInfo(MethodView):
    @jwt_required()
    @blp.arguments(CartSchema)
    @blp.response(200, CartSchema)
    def post(self, product):
        user_id = int(get_jwt_identity())  
        data = ProductModel.query.filter_by(id = product["product_id"]).first()
        if not data:
            abort (404, message = "Product DoestNot Exsist")
        cart = CartModel(user_id = user_id, product_id = product["product_id"], quantity = product["quantity"])
        db.session.add(cart)
        db.session.commit()
        return cart

    @jwt_required()
    @blp.response(200, CartSchema(many = True))
    def get(self):
        user_id = int(get_jwt_identity())
        cart_item = CartModel.query.filter_by(user_id = user_id).all()
        return cart_item