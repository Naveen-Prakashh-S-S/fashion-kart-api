from db import db

class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),  nullable = False)
    price = db.Column(db.Integer,nullable = False)

    tags = db.relationship("TagsModel", secondary = "product_tags", back_populates = "products")

    sizes = db.relationship( "ProductSizeModel" , back_populates="product")