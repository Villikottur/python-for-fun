import random
from flask import Blueprint, jsonify, make_response, request
from flask_restful import Api, Resource, abort
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, update
import misc
from database import db
from db_models import RoomModel, DoorModel, UserModel
from resources_schemas import RoomSchema, DoorSchema, ItemSchema, UserSchema
from exception_handler import handle_exceptions

rooms_blp = Blueprint("rooms", __name__, url_prefix="/room")
rooms_api = Api(rooms_blp)


@rooms_api.resource("/begin/entrance_hall")
class EntranceHall(Resource):
    @handle_exceptions(RoomSchema())
    @jwt_required()
    def get(self) -> object:
        schema = RoomSchema()
        username = misc.get_jwt_username()
        db_user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        if db_user.hearts < 1 or not db_user.is_alive:
            abort(
                400,
                message="You're dead. You cannot do anything (except decomposing).",
            )
        current_room = misc.get_current_room(username=username)
        if (
            current_room != None
            and current_room != "first_room"
            and current_room != "entrance_hall"
        ):
            abort(400, message="You cannot teleport to entrance_hall.")
        room = db.session.query(RoomModel).filter(RoomModel.id == 1).first()
        db.session.execute(
            update(UserModel)
            .where(UserModel.username == username)
            .values(current_room="entrance_hall")
        )
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "room": schema.dump(room),
                    "message": "You've entered the Entrance Hall. It's cold. It's dark. Shadows stretch long and blurred...",
                    "hint": "Choose a door and send a GET to /room/your_room/door_ID",
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>")
class RoomAccess(Resource):
    @handle_exceptions(RoomSchema())
    @jwt_required()
    def get(self, room_name: str) -> object:
        hearts_message = None
        defence_message = None
        username = misc.get_jwt_username()
        db_user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        if db_user.hearts < 1:
            abort(
                400,
                message="You're dead. You cannot do anything (except decomposing).",
            )
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(
                400,
                message="You cannot access that room. As far as I know, you cannot teleport (yet).",
            )
        db_current_room = (
            db.session.query(RoomModel).filter(RoomModel.name == current_room).first()
        )
        if not db_current_room.lights_on and not db_current_room.entity:
            if random.random() < 0.3:
                db_current_room.entity = random.choice(
                    ["ghost", "witch", "zombie", "vampire"]
                )
        entity = db_current_room.entity
        if (
            not db_current_room.lights_on
            and db_current_room.entity
            and not db_user.weapon
        ):
            db_user.hearts -= 1
            hearts_message = f"A {entity} attacked you! You lost one heart!"
        if not db_current_room.lights_on and db_current_room.entity and db_user.weapon:
            db_user.weapon = False
            db_current_room.entity = None
            defence_message = f"A {entity} attacked you! You defended yourself with your weapon (got destroyed in the fight though)!"
        db_target_room = (
            db.session.query(RoomModel).filter(RoomModel.name == room_name).first()
        )
        common_door = set(
            [
                db_current_room.north_exit_id,
                db_current_room.east_exit_id,
                db_current_room.south_exit_id,
                db_current_room.west_exit_id,
            ]
        ) & set(
            [
                db_target_room.north_exit_id,
                db_target_room.east_exit_id,
                db_target_room.south_exit_id,
                db_target_room.west_exit_id,
            ]
        )
        common_door.discard(None)
        if not common_door:
            abort(
                400,
                message="You cannot access that room. As far as I know, you cannot teleport (yet).",
            )
        common_door = common_door.pop()
        db_door = (
            db.session.query(DoorModel).filter(DoorModel.id == common_door).first()
        )
        if db_door:
            if db_door.is_locked:
                abort(
                    400,
                    message="The door is locked.",
                    hint="If only you could find a key...",
                )
            if not db_door.is_open:
                abort(400, message="The door is closed.")
            user = (
                db.session.query(UserModel)
                .filter(UserModel.username == username)
                .first()
            )
            user.current_room = room_name
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "room": RoomSchema().dump(db_target_room),
                    "message": misc.custom_messages_by_room[f"{room_name}"],
                    "hint": "Choose a door and send a GET to /room/your_room/door_ID",
                    "attack": hearts_message,
                    "defence": defence_message,
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>/<int:door_id>")
class DoorInfo(Resource):
    @handle_exceptions(DoorSchema())
    @jwt_required()
    def get(self, room_name: str, door_id: int) -> object:
        username = misc.get_jwt_username()
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        schema = DoorSchema()
        rooms = (
            db.session.query(RoomModel)
            .filter(
                or_(
                    RoomModel.north_exit_id == door_id,
                    RoomModel.east_exit_id == door_id,
                    RoomModel.south_exit_id == door_id,
                    RoomModel.west_exit_id == door_id,
                )
            )
            .all()
        )
        rooms_names = [room.name for room in rooms]
        door = db.session.query(DoorModel).filter(DoorModel.id == door_id).first()
        if len(rooms_names) == 2:
            return (
                make_response(
                    jsonify(
                        {
                            "door": schema.dump(door),
                            "message": f"This door leads to either {rooms_names[0]} or {rooms_names[1]}.",
                            "hint": "Choose a room and... GET it.",
                        }
                    ),
                    200,
                )
                if len(rooms_names) == 2
                else make_response(
                    jsonify(
                        {
                            "door": schema.dump(door),
                            "message": f"This door leads to {rooms_names[0]}.",
                            "hint": "Choose a room and... GET it.",
                        }
                    ),
                    200,
                )
            )


@rooms_api.resource("/<string:room_name>/<int:door_id>/key")
class DoorLock(Resource):
    @handle_exceptions(DoorSchema())
    @jwt_required()
    def put(self, room_name: str, door_id: int) -> object:
        username = misc.get_jwt_username()
        user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        user_items = set(user.items.split(",")) if user.items else set()
        if not user.items:
            abort(
                400,
                messsage="According to physics, you cannot unlock a door without a key.",
            )
        if "key" not in user.items:
            abort(
                400,
                message="According to physics, you cannot unlock a door without a key.",
            )
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        schema = DoorSchema()
        door = db.session.query(DoorModel).filter(DoorModel.id == door_id).first()
        door.is_locked = False
        user_items.discard("key")
        user.items = ",".join(user_items) if user_items else None
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "door": schema.dump(door),
                    "message": f"You unlocked the door.",
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>/lights")
class Lights(Resource):
    @handle_exceptions(RoomSchema())
    @jwt_required()
    def get(self, room_name: str) -> object:
        username = misc.get_jwt_username()
        current_room = misc.get_current_room(username=username)
        schema = RoomSchema()
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        room = db.session.query(RoomModel).filter(RoomModel.name == room_name).first()
        room.lights_on = True
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "room": schema.dump(room),
                    "message": f"You switch on the lights.",
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>/<int:door_id>/open")
class DoorOpen(Resource):
    @handle_exceptions(DoorSchema())
    @jwt_required()
    def put(self, room_name: str, door_id: int) -> object:
        door = db.session.query(DoorModel).filter(DoorModel.id == door_id).first()
        if door.is_locked:
            abort(400, message="The door is locked.")
        username = misc.get_jwt_username()
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        schema = DoorSchema()
        door.is_open = True
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "door": schema.dump(door),
                    "message": f"You opened the door.",
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>/pick_up")
class ItemPickUp(Resource):
    @handle_exceptions(UserSchema)
    @jwt_required()
    def put(self, room_name) -> object:
        username = misc.get_jwt_username()
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        schema = ItemSchema()
        put_data = schema.load(request.get_json())
        room = (
            db.session.query(RoomModel).filter(RoomModel.name == current_room).first()
        )
        room_items = set(room.items.split(",") if room.items else set())
        if not room.items:
            abort(400, message="There's nothing to pick up.")
        user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        user_items = set(user.items.split(",") if user.items else set())
        items_to_pick_up = set(room.items.split(",")) & set(
            put_data["items"].split(",")
        )
        if any(
            item in {"gun", "sword", "hammer", "knife"} for item in items_to_pick_up
        ):
            user.weapon = True
            room_items -= items_to_pick_up
            items_to_pick_up -= {"gun", "sword", "hammer", "knife"}
        room_items -= items_to_pick_up
        user_items |= items_to_pick_up
        room.items = ",".join(room_items) if room_items else None
        user.items = ",".join(user_items)
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "room": RoomSchema().dump(room),
                    "message": f"You picked up {put_data['items']}.",
                    "user": UserSchema().dump(user),
                }
            ),
            200,
        )


@rooms_api.resource("/<string:room_name>/drop")
class ItemDrop(Resource):
    @handle_exceptions(RoomSchema())
    @jwt_required()
    def put(self, room_name) -> object:
        username = misc.get_jwt_username()
        current_room = misc.get_current_room(username=username)
        if not current_room:
            abort(400, message=f"You cannot teleport (yet).")
        elif room_name != current_room:
            abort(
                400, message=f"You cannot teleport. You're currently in {current_room}"
            )
        schema = ItemSchema()
        put_data = schema.load(request.get_json())
        room = (
            db.session.query(RoomModel).filter(RoomModel.name == current_room).first()
        )
        room_items = set(room.items.split(",") if room.items else set())
        user = (
            db.session.query(UserModel).filter(UserModel.username == username).first()
        )
        user_items = set(user.items.split(",")) if user.items else set()
        items_to_drop = set(put_data["items"].split(","))
        room_items |= items_to_drop
        user_items -= items_to_drop
        room.items = ",".join(room_items)
        user.items = ",".join(user_items) if user_items else None
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "room": RoomSchema().dump(room),
                    "message": f"You dropped {put_data['items']}.",
                    "user": UserSchema().dump(user),
                }
            ),
            200,
        )
