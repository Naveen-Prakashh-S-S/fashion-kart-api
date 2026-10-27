
from db import db


class OrderItemModel(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False )
    size_id = db.Column(db.Integer, nullable=False )
    product_id = db.Column( db.Integer, db.ForeignKey("products.id"),  nullable=False )
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float, nullable=False)
    order = db.relationship("OrderModel",back_populates="items")
