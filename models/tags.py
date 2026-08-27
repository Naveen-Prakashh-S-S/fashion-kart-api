from db import db

class TagsModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)

    products = db.relationship( "ProductModel", secondary="product_tags", back_populates="tags" )