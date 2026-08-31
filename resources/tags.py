from db import db
from models import TagsModel
from schemas import PlainTagSchema, TagSchema, TagCreateSchema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description = "Operation on Tags")

@blp.route("/admin/tags")
class TagsBasic(MethodView):
    #Create One New tag form the JSON Input
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
    
    #Get All the Tags created 
    @blp.response(200, TagSchema(many = True))
    def get(self):
        return TagsModel.query.all()

@blp.route("/admin/tags/<int:tag_id>")
class SingleTag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        return tag
    
    @blp.arguments(TagCreateSchema)
    @blp.response(200, TagSchema)
    def put(self,tag_data ,tag_id):
        tag = TagsModel.query.get(tag_id)
        if tag :
            tag.name = tag_data["name"]
        else:
            abort(404, message = "Tag is not Exist in DataBase")
        db.session.add(tag)
        db.session.commit()
        return tag

    def delete(self, tag_id):
        tag = TagsModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {"Message" : "Item Deleted"}
            
