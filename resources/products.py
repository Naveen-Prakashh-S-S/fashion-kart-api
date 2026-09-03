from db import db
from models import ProductModel, ProductTagModel, ProductSizeModel, TagsModel, SizeModel
from schemas import ProductSizeSchema, ProductSizeCreateSchema, ProductCreateSchema, ProductSchema, PlainProductSchema , ProductTagCreateSchema, ProductAddSize, ProductStockUpdateSchema
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

    @blp.response(200, ProductSchema(many = True))
    def get(self):
        return ProductModel.query.all()

@blp.route("/admin/products/<int:product_id>")
class GetOneProduct(MethodView):
    @blp.response(201, ProductSchema)
    def get(self, product_id):
        return ProductModel.query.get_or_404(product_id)
    
    @blp.arguments(ProductCreateSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        try:
            # Get Product
            product = ProductModel.query.get_or_404(product_id)
            # Validate Tags
            tags = []
            for tag_id in product_data["tags"]:
                tag = TagsModel.query.get(tag_id)
                if not tag:
                    abort(400,message=f"Tag ID {tag_id} does not exist")
                tags.append(tag)
            # Validate Sizes
            for size_data in product_data["sizes"]:
                size = SizeModel.query.get(size_data["size_id"])
                if not size:
                    abort(
                        400,
                        message=f"Size ID {size_data['size_id']} does not exist"
                    )
            # Update Product
            product.name = product_data["name"]
            product.price = product_data["price"]
            # Update Tags
            product.tags = tags
            # Remove Old Product Sizes
            ProductSizeModel.query.filter_by(
                product_id=product_id
            ).delete()
            # Add New Product Sizes
            for size_data in product_data["sizes"]:
                product_size = ProductSizeModel(
                    product_id=product_id,
                    size_id=size_data["size_id"],
                    stock=size_data["stock"]
                )
                db.session.add(product_size)
            # Save
            db.session.commit()
            return product
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Failed to update Product")

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        product_tags = ProductTagModel.query.filter_by(product_id = product_id).all()
        for product_tag in product_tags :
            db.session.delete(product_tag)

        product_sizes = ProductSizeModel.query.filter_by(product_id = product_id).all()

        for product_size in product_sizes:
            db.session.delete(product_size)

        db.session.delete(product)
        db.session.commit()
        return {"Message" : "Deleted Successfully.."}

@blp.route("/admin/products/<int:product_id>/sizes")
class ProductSize(MethodView):
    @blp.arguments(ProductAddSize)
    @blp.response(200)
    def post(self, size_data, product_id):
        #Check Already Size is Added Or Not
        size = ProductSizeModel.query.filter_by(product_id = product_id, size_id = size_data["id"]).first()
        if size :
            abort(400, message = "FAILED: Size is Already added to Product...")
        product = ProductModel.query.filter_by(id = product_id).first_or_404()
        product_size = ProductSizeModel(product_id = product.id, size_id = size_data["id"], stock = size_data["stock"])
        db.session.add(product_size)
        db.session.commit()
        return {"Message" : "Size Successfully Added to Product..."}

#Check Once for Unique Data to Add
@blp.route("/admin/products/<int:product_id>/tags")
class ProductTag(MethodView):
    @blp.arguments(ProductTagCreateSchema)
    @blp.response(200, ProductSchema)
    def post(self, tag_data, product_id):
        product = ProductModel.query.get_or_404(product_id)
        tag = TagsModel.query.get_or_404(tag_data["id"])
        product.tags.append(tag)
        db.session.commit()
        return product

@blp.route("/admin/products/<int:product_id>/tags/<int:tag_id>")
class ProductTagRemove(MethodView):
    def delete(self, product_id, tag_id):
        product_tag = ProductTagModel.query.filter_by(product_id = product_id, tag_id = tag_id).first_or_404()
        db.session.delete(product_tag)
        db.session.commit()
        return {"Message" : "Tag Removed from Product Successfully..."}


@blp.route("/admin/products/<int:product_id>/sizes/<int:size_id>/stock")
class UpdateProductStock(MethodView):
    @blp.arguments(ProductStockUpdateSchema)
    def patch(self, stock_data, product_id, size_id):
        size = ProductSizeModel.query.filter_by(product_id = product_id, size_id = size_id).first_or_404()
        size.stock = stock_data["stock"]
        db.session.add(size)
        db.session.commit()
        return {"Message" : f"Stock of the Size Updated in Product.."}
        
@blp.route("/admin/products/<int:product_id>/sizes/<int:size_id>")
class RemoveSizeFromProduct(MethodView):
    @blp.response(200)
    def delete(self, product_id, size_id):
        product_size = ProductSizeModel.query.filter_by(product_id = product_id, size_id = size_id).first_or_404()
        db.session.delete(product_size)
        db.session.commit()
        return {"Message" : "DONE: Size Removed from Product.."}