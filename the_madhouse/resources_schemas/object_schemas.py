from marshmallow import Schema, fields


class DoorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    is_open = fields.Bool()
    is_locked = fields.Bool()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
    current_room = fields.Str()
    items = fields.Str()
    weapon = fields.Bool()
    hearts = fields.Int()
    is_alive = fields.Bool()
    knocks = fields.Int()


class RoomSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    lights_on = fields.Bool()
    items = fields.Str(allow_none=True)
    entity = fields.Str(allow_none=True)
    north_exit_id = fields.Int(allow_none=True)
    east_exit_id = fields.Int(allow_none=True)
    south_exit_id = fields.Int(allow_none=True)
    west_exit_id = fields.Int(allow_none=True)


class ItemSchema(Schema):
    items = fields.Str()
