from db import db

class CartModel(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable = False)

    quantity = db.Column(db.Integer, nullable = False , default = 1)