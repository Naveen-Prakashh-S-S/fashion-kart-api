from db import db
from models import TagsModel
from schemas import PlainTagSchema, TagSchema, TagCreateSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description = "Operation on Tags")

@blp.route("/admin/tags")
class TagsBasic(MethodView):
    @blp.arguments(TagCreateSchema)
    @blp.response(201, PlainTagSchema)
    def post(self, tag_data):
        tag = TagsModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))
        return tag