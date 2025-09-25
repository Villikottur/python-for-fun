from database import db


class DoorModel(db.Model):
    __tablename__ = "doors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    is_open = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default="player")
    current_room = db.Column(db.String)
    items = db.Column(db.String, default=None)
    weapon = db.Column(db.Boolean, default=False)
    hearts = db.Column(db.Integer, default=5, nullable=False)
    is_alive = db.Column(db.Boolean, default=True)


class RoomModel(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    lights_on = db.Column(db.Boolean, default=False)
    items = db.Column(db.String)
    entity = db.Column(db.String)
    north_exit_id = db.Column(db.Integer, db.ForeignKey("doors.id"))
    east_exit_id = db.Column(db.Integer, db.ForeignKey("doors.id"))
    south_exit_id = db.Column(db.Integer, db.ForeignKey("doors.id"))
    west_exit_id = db.Column(db.Integer, db.ForeignKey("doors.id"))
    north_exit = db.relationship("DoorModel", foreign_keys=[north_exit_id])
    east_exit = db.relationship("DoorModel", foreign_keys=[east_exit_id])
    south_exit = db.relationship("DoorModel", foreign_keys=[south_exit_id])
    west_exit = db.relationship("DoorModel", foreign_keys=[west_exit_id])


class TokenModel(db.Model):
    __tablename__ = "tokens"
    username = db.Column(db.String, db.ForeignKey("users.username"), primary_key=True)
    user = db.relationship("UserModel", foreign_keys=[username])
    token = db.Column(db.String, primary_key=True)
    is_expired = db.Column(db.Boolean, default=False)
