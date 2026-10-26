
from db import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending"
    )

    total_price = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    items = db.relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan"
    )
