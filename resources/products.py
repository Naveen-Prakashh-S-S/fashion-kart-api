from db import db
from models import ProductModel, ProductTagModel, ProductSizeModel
from schemas import ProductSizeSchema, ProductSizeCreateSchema, ProductCreateSchema, ProductSchema, PlainProductSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Products", "products", description = "Operation on Products")

@blp.route("/admin/products")
class ProductBasic(MethodView):
    @blp.arguments(ProductCreateSchema)
    @blp.response(200, ProductSchema)
    def post(self, product_data):
        try:
            # validate Tag Existence 
            for tag_id in product_data["tags"]:
                tag = TagsModel.query.get(tag_id)
                if not tag:
                    abort(400,message=f"Tag ID {tag_id} does not exist")
            #VaLidate Size Existence    
            for size_data in product_data["sizes"]:
                size_id = size_data["size_id"]
                size = SizeModel.query.get(size_id)
                if not size:
                    abort(400,message=f"Size ID {size_id} does not exist")
            # Create Product
            product = ProductModel ( name = product_data [ "name" ], price = product_data [ "price" ])
            db.session.add(product)

            #Get Product ID
            db.session.flush()

            #Add Tags

            for tag_id in product_data["tags"]:
                product_tag = ProductTagModel(product_id = product.id, tag_id = tag_id)
                db.session.add(product_tag)

            #Add Size and Stock

            for size_data in product_data["sizes"]:
                product_size = ProductSizeModel(product_id = product.id, size_id = size_data["size_id"], stock = size_data["stock"])
                db.session.add(product_size)

            db.session.commit()

            return product
        except SQLAlchemyError:

            db.session.rollback()
            abort(500, message = "Failed To Create Product")