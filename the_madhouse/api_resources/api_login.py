from flask import Blueprint, jsonify, make_response, request
from flask_restful import Api, Resource, abort
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)
from passlib.hash import pbkdf2_sha256
from resources_schemas import UserSchema
from db_models import UserModel, TokenModel
from database import db
from exception_handler import handle_exceptions
import misc

login_blp = Blueprint("login", __name__)
login_api = Api(login_blp)

frontdoor_blp = Blueprint("front_door", __name__)
frontdoor_api = Api(frontdoor_blp)


@login_api.resource("/login")
class Login(Resource):
    def get(self) -> object:
        return make_response(
            jsonify(
                {
                    "message": "Welcome to the login endpoint.",
                    "description": (
                        "In front of you there's an old, big, dark, run down door."
                        " Please use a POST request on /frontdoor to enter, if you dare."
                        " This is the start of your game. Good luck."
                    ),
                    "hint": "Make sure to knock a few times in your JSON...",
                }
            ),
            200,
        )


@login_api.resource("/login/restart")
class Restart(Resource):
    def get(self) -> object:
        return make_response(
            jsonify(
                {
                    "message": "And so you wanna try again...",
                    "hint": "Send a POST request and include your refresh token.",
                }
            ),
            200,
        )

    @handle_exceptions(schema=UserSchema)
    @jwt_required(refresh=True)
    def post(self) -> object:
        identity = get_jwt_identity()
        new_token = create_access_token(identity=identity)
        user = (
            db.session.query(UserModel)
            .filter(UserModel.username == misc.get_jwt_username())
            .first()
        )
        user_token = (
            db.session.query(TokenModel)
            .filter(TokenModel.username == misc.get_jwt_username())
            .first()
        )
        user.hearts = 5
        user.is_alive = True
        user_token.token = new_token
        user_token.is_expired = False
        db.session.commit()
        return make_response(
            jsonify(
                user_data=UserSchema().dump(user),
                access_token=new_token,
                message=f"Here's your new token. Have fun (if you dare).",
            ),
            201,
        )


@frontdoor_api.resource("/frontdoor")
class Frontdoor(Resource):
    @handle_exceptions(schema=UserSchema())
    def post(self) -> object:
        schema = UserSchema()
        post_data = schema.load(request.get_json())
        if "knocks" not in post_data:
            abort(
                400,
                message="Nothing happens. Maybe try again with one more or fewer knocks...",
            )
        knock_count = post_data["knocks"]
        post_data.pop("knocks", None)
        if knock_count == 6:
            post_data["password"] = pbkdf2_sha256.hash(post_data["password"])
            new_user = UserModel(**post_data)
            db.session.add(new_user)
            access_token = create_access_token(
                identity={"username": post_data["username"]},
                fresh=True,
            )
            refresh_token = create_refresh_token(
                identity={"username": post_data["username"]}
            )
            new_token_row = TokenModel(username=new_user.username, token=access_token)
            db.session.add(new_token_row)
            db.session.commit()
            return make_response(
                jsonify(
                    user_data=schema.dump(new_user),
                    access_token=access_token,
                    refresh_token=refresh_token,
                    message=f"The door opens. Welcome, {post_data['username']}."
                    " This is your token (and refresh) for the game. Save it or you're fucked."
                    " Use GETs to explore the place."
                    " Step into room/begin/entrance_hall and find out what's next."
                    " Oh, also: you have 10 minutes starting from now."
                    " If you can't find the exit within this time, you're dead."
                    " And you cannot run away. At all.",
                ),
                201,
            )
        abort(
            400,
            message="Nothing happens. Maybe try again with one more or fewer knocks...",
        )
