from db import db

class ProductTagModel(db.Model):
    __tablename__ = "product_tags"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key = True)