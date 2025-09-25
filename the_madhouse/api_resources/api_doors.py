from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from resources_schemas import DoorSchema
from database import db
from db_models import DoorModel
from exception_handler import handle_exceptions

doors_blp = Blueprint("doors", __name__, url_prefix="/door")
doors_api = Api(doors_blp)


@doors_api.resource("s")
class Doors(Resource):
    @handle_exceptions(DoorSchema())
    def get(self) -> object:
        schema = DoorSchema(many=True)
        doors = DoorModel.query.all()
        return make_response(jsonify(schema.dump(doors)), 200)

    @handle_exceptions(DoorSchema())
    def post(self) -> object:
        resource_schema = DoorSchema
        schema = resource_schema(many=True)
        post_data = schema.load(request.get_json())
        new_doors = [DoorModel(**data) for data in post_data]
        db.session.add_all(new_doors)
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "message": "New doors added successfully.",
                    "data": schema.dump(new_doors),
                }
            ),
            201,
        )
