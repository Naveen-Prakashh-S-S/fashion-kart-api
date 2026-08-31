from db import db
from models import SizeModel
from schemas import SizeCreateSchema,  PlainSizeSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Sizes", "sizes", description = "Operation on Sizes")

@blp.route("/admin/sizes")
class SizeBasics(MethodView):
    @blp.arguments(SizeCreateSchema)
    @blp.response(200, PlainSizeSchema)
    def post(self, size_data):
        size = SizeModel(**size_data)
        try:
            db.session.add(size)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))
        return size
    @blp.response(200, PlainSizeSchema(many = True))
    def get(self):
        return SizeModel.query.all()


@blp.route("/admin/sizes/<int:size_id>")
class SingleSize(MethodView):
    @blp.response(200, PlainSizeSchema)
    def get(self, size_id):
        return SizeModel.query.get_or_404(size_id)

    @blp.arguments(SizeCreateSchema)
    @blp.response(200, PlainSizeSchema)
    def put(self, size_data, size_id):
        size = SizeModel.query.get(size_id)
        if size :
            size.name = size_data["name"]
        else:
            abort(404, message = "Size is not Exist in DataBase..")
        db.session.add(size)
        db.session.commit()
        return size
    def delete(self, size_id):
        tag = SizeModel.query.get_or_404(size_id)
        db.session.delete(tag)
        db.session.commit()
        return {"Message" : "Item Deleted"}
