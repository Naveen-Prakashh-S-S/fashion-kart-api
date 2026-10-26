from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from models.cart import CartModel
from models import ProductModel
from models import OrderModel
from models import OrderItemModel
from schemas import OrderSchema

# Use your existing order blueprint if you already have one.

blp = Blueprint("Orders", "orders", description = "Operation on Orders")


@blp.route("/order")
class OrderResource(MethodView):

    @jwt_required()
    @blp.response(201, OrderSchema)
    def post(self):
       user_id = int(get_jwt_identity())

       cart_items = CartModel.query.filter_by(user_id = user_id).all()

       if not cart_items:
           abort(400, message = "Cart is Items")

       order = OrderModel(user_id = user_id, status = "pending", total_price = 0)

       total_price = 0
       try:
            for cart_item in cart_items:
                product = ProductModel.query.get(
                    cart_item.product_id
                )

                if not product:
                    abort(400, message="A product in your cart no longer exists")

                price = product.price
                quantity = cart_item.quantity

                order_item = OrderItemModel(
                    product_id=product.id,
                    quantity=quantity,
                    price=price
                )

                order.items.append(order_item)
                total_price += price * quantity

            order.total_price = total_price

            db.session.add(order)
            db.session.flush()

            for cart_item in cart_items:
                db.session.delete(cart_item)

            db.session.commit()

       except Exception:
            db.session.rollback()
            raise

       return order