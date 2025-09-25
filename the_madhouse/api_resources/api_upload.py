import os
from flask import Blueprint, request, abort, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from resources_schemas import UploadSchema

uploads_blp = Blueprint("uploads", __name__, url_prefix="/upload")
uploads_api = Api(uploads_blp)


@uploads_api.resource("")
class Uploads(Resource):
    resource_schema = UploadSchema

    @jwt_required()
    def post(self) -> object:
        schema = self.resource_schema()
        try:
            file = request.files.get("file")
            schema.load({"file": file})
        except ValidationError:
            return abort(400, message="Please provide a valid .txt file.")
        except Exception as e:
            return abort(400, message=f"{str(e)}")
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        grandparent_dir = os.path.dirname(parent_dir)
        file_path = f"{grandparent_dir}\\uploads\\{file.filename}"
        file.save(file_path)
        try:
            with open(file_path, "r") as f:
                content = f.read().lower()
                if "death" in content:
                    return make_response(
                        jsonify(
                            {
                                "message": "That's it. You won. Now please disappear and leave me alone.",
                            }
                        ),
                        200,
                    )
        except Exception as e:
            return abort(400, "Something is wrong with your file. Please try again.")
        return make_response(
            jsonify(
                {
                    "message": f"File uploaded correctly, but... wrong answer. Try again or stay here forever.",
                }
            ),
            200,
        )
