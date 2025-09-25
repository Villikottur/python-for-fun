from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource, abort
from flask_jwt_extended import jwt_required
import misc
from database import db
from db_models import UserModel
from resources_schemas import UserSchema
from exception_handler import handle_exceptions

hearts_blp = Blueprint("hearts", __name__, url_prefix="/hearts")
hearts_api = Api(hearts_blp)


@hearts_api.resource("")
class Hearts(Resource):
    @jwt_required()
    @handle_exceptions(UserSchema)
    def get(self) -> object:
        username = misc.get_jwt_username()
        db_user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        if not db_user.items:
            abort(400, message="You have no items.")
        item_list = db_user.items.split(",")
        if "heart" in item_list:
            db_user.hearts += 1
            item_list.remove("heart")
            db_user.items = ",".join(item_list) if item_list else None
            db.session.commit()
        return make_response(
            jsonify(
                {
                    "user": UserSchema().dump(db_user),
                    "message": "You used a heart!",
                }
            ),
            200,
        )
