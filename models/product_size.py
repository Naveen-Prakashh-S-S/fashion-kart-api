from db import db

class ProductSizeModel(db.Model):
    __tablename__ = "product_sizes"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key = True)
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"), primary_key = True)
    stock = db.Column(db.Integer, nullable = False, default = 0 )

    product = db.relationship( "ProductModel", back_populates="sizes" )
    size = db.relationship( "SizeModel" )