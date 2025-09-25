import jwt, app as app
from flask import request
from typing import Optional
from database import db
from db_models import UserModel

custom_messages_by_room = {
    "eerie_parlor": "A dimly lit room. Antique furniture seems to move when you're not looking.",
    "phantom_livingroom": "The fireplace crackles… even when unlit.",
    "vanishing_diningroom": "Plates shift, chairs scrape, but no one's around.",
    "wraith_kitchen": "The scent of burnt offerings lingers in the air.",
    "bloodstained_pantry": "Jars of something red, but it's not jam…",
    "shadow_staircase": "No matter how many times you count, there's always one extra step.",
    "widows_bedroom": "A four-poster bed where someone unseen still sleeps.",
    "rotting_nursery": "The rocking horse creaks, though no child remains.",
    "whispering_guestroom": "Stay the night, and you might hear your name… from inside the walls.",
    "bleeding_bathroom": "The mirror shows things that aren't behind you.",
    "forgotten_library": "Books open to pages on their own, warning of past horrors.",
    "cobweb_chamber": "A room untouched for decades, but fresh footprints in the dust.",
    "hollow_loft": "Something scurries just beneath the wooden floorboards.",
    "toy_room": "Dolls with missing eyes that seem to stare anyway.",
    "attic_of_echoes": "Every word you speak is repeated… by a voice that isn't yours.",
    "bone_storage": "Wooden crates filled with… well, you don't want to check.",
    "boiler_room": "Chains swing from the ceiling, but who left them there?",
    "moonlit_greenhouse": "Overgrown plants that breathe in unison.",
    "endless_hall": "A corridor that always seems one door longer than before.",
    "supersecretroom": "And so you've managed to come here. I'll let you go. But first, you have to solve this riddle: I am a shadow that follows you, yet you cannot see me. I am a visitor that comes uninvited, and a guest that never leaves. What am I? Send me your answer on /upload.",
    "mausoleum_room": "A place to sit, if you don't mind the company of the long-dead.",
    "room_that_isnt_there": "Sometimes it's in the blueprints, sometimes it's not.",
}


def get_jwt_username() -> str:
    """Retrieves the username of a player with the token as input

    :return: Username of the player
    :rtype: str"""
    token = request.headers.get(key="Authorization").split(sep="Bearer ")[1]
    decoded_token = jwt.decode(
        jwt=token, key=app.FlaskConfig.JWT_SECRET_KEY, algorithms=["HS256"]
    )
    username = decoded_token.get("sub", {}).get("username")
    return username


def get_current_room(username: str) -> Optional[str]:
    """Retrieves the room the player is currently in

    :return: The room where the player is at the moment
    :rtype: str"""
    current_room = (
        db.session.query(UserModel.current_room)
        .filter(UserModel.username == username)
        .scalar()
    )
    return current_room
