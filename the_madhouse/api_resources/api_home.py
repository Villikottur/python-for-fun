from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource

welcome_blp = Blueprint("welcome", __name__)
welcome_api = Api(welcome_blp)


@welcome_api.resource("/")
class Welcome(Resource):
    def get(self) -> object:
        return make_response(
            jsonify(
                {
                    "message": "Welcome to the Madhouse!",
                    "description": (
                        "Hello there and welcome (or should I say run while you still can?)."
                        " This is the Madhouse, a twisted and degenerate game that will try your patience and your guts as well."
                        " If you wanna start, please just visit the /login endpoint."
                    ),
                }
            ),
            200,
        )
