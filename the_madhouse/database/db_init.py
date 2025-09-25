from database import db
from db_models import DoorModel, RoomModel


def init_db():
    room1 = RoomModel(
        id=1,
        name="entrance_hall",
        items="key,sword,mirror",
        north_exit_id=17,
        east_exit_id=13,
        south_exit_id=None,
        west_exit_id=None,
    )
    room2 = RoomModel(
        id=2,
        name="eerie_parlor",
        items="candle,picture",
        north_exit_id=15,
        east_exit_id=None,
        south_exit_id=17,
        west_exit_id=None,
    )
    room3 = RoomModel(
        id=3,
        name="phantom_livingroom",
        items="bag,painting",
        north_exit_id=None,
        east_exit_id=22,
        south_exit_id=None,
        west_exit_id=13,
    )
    room4 = RoomModel(
        id=4,
        name="vanishing_diningroom",
        items="",
        north_exit_id=None,
        east_exit_id=71,
        south_exit_id=None,
        west_exit_id=22,
    )
    room5 = RoomModel(
        id=5,
        name="wraith_kitchen",
        items="knife,key",
        north_exit_id=None,
        east_exit_id=88,
        south_exit_id=None,
        west_exit_id=71,
    )
    room6 = RoomModel(
        id=6,
        name="bloodstained_pantry",
        items="jar",
        north_exit_id=None,
        east_exit_id=None,
        south_exit_id=None,
        west_exit_id=88,
    )
    room7 = RoomModel(
        id=7,
        name="shadow_staircase",
        items="",
        north_exit_id=30,
        east_exit_id=None,
        south_exit_id=15,
        west_exit_id=None,
    )
    room8 = RoomModel(
        id=8,
        name="widows_bedroom",
        items="key,book",
        north_exit_id=50,
        east_exit_id=60,
        south_exit_id=30,
        west_exit_id=None,
    )
    room9 = RoomModel(
        id=9,
        name="rotting_nursery",
        items="heart,toy",
        north_exit_id=None,
        east_exit_id=70,
        south_exit_id=None,
        west_exit_id=60,
    )
    room10 = RoomModel(
        id=10,
        name="whispering_guestroom",
        items="",
        north_exit_id=27,
        east_exit_id=None,
        south_exit_id=50,
        west_exit_id=None,
    )
    room11 = RoomModel(
        id=11,
        name="bleeding_bathroom",
        items="needle,book",
        north_exit_id=33,
        east_exit_id=None,
        south_exit_id=27,
        west_exit_id=36,
    )
    room12 = RoomModel(
        id=12,
        name="forgotten_library",
        items="needle,book",
        north_exit_id=99,
        east_exit_id=None,
        south_exit_id=None,
        west_exit_id=70,
    )
    room13 = RoomModel(
        id=13,
        name="cobweb_chamber",
        items="spiderweb,book",
        north_exit_id=11,
        east_exit_id=None,
        south_exit_id=99,
        west_exit_id=None,
    )
    room14 = RoomModel(
        id=14,
        name="hollow_loft",
        items="key,candle",
        north_exit_id=None,
        east_exit_id=36,
        south_exit_id=None,
        west_exit_id=40,
    )
    room15 = RoomModel(
        id=15,
        name="toy_room",
        items="toy,heart",
        north_exit_id=56,
        east_exit_id=40,
        south_exit_id=None,
        west_exit_id=None,
    )
    room16 = RoomModel(
        id=16,
        name="attic_of_echoes",
        items="",
        north_exit_id=None,
        east_exit_id=None,
        south_exit_id=56,
        west_exit_id=None,
    )
    room17 = RoomModel(
        id=17,
        name="bone_storage",
        items="bone,key",
        north_exit_id=66,
        east_exit_id=None,
        south_exit_id=11,
        west_exit_id=None,
    )
    room18 = RoomModel(
        id=18,
        name="boiler_room",
        items="chains",
        north_exit_id=None,
        east_exit_id=42,
        south_exit_id=66,
        west_exit_id=None,
    )
    room19 = RoomModel(
        id=19,
        name="moonlit_greenhouse",
        items="plant,heart",
        north_exit_id=96,
        east_exit_id=None,
        south_exit_id=None,
        west_exit_id=42,
    )
    room20 = RoomModel(
        id=20,
        name="endless_hall",
        items="key",
        north_exit_id=69,
        east_exit_id=None,
        south_exit_id=96,
        west_exit_id=None,
    )
    room21 = RoomModel(
        id=21,
        name="supersecretroom",
        items="",
        entity="cheshire_cat",
        north_exit_id=None,
        east_exit_id=None,
        south_exit_id=69,
        west_exit_id=None,
    )
    room22 = RoomModel(
        id=22,
        name="mausoleum_room",
        items="key,statue",
        north_exit_id=79,
        east_exit_id=None,
        south_exit_id=33,
        west_exit_id=None,
    )
    room23 = RoomModel(
        id=23,
        name="room_that_isnt_there",
        items="heart",
        north_exit_id=None,
        east_exit_id=None,
        south_exit_id=79,
        west_exit_id=None,
    )
    door13 = DoorModel(id=13, name="Num13", is_locked=False)
    door22 = DoorModel(id=22, name="Num22", is_locked=False)
    door71 = DoorModel(id=71, name="Num71", is_locked=False)
    door88 = DoorModel(id=88, name="Num88", is_locked=True)
    door17 = DoorModel(id=17, name="Num17", is_locked=True)
    door15 = DoorModel(id=15, name="Num15", is_locked=False)
    door30 = DoorModel(id=30, name="Num30", is_locked=False)
    door60 = DoorModel(id=60, name="Num60", is_locked=False)
    door70 = DoorModel(id=70, name="Num70", is_locked=False)
    door99 = DoorModel(id=99, name="Num99", is_locked=False)
    door11 = DoorModel(id=11, name="Num11", is_locked=False)
    door66 = DoorModel(id=66, name="Num66", is_locked=False)
    door42 = DoorModel(id=42, name="Num42", is_locked=False)
    door96 = DoorModel(id=96, name="Num96", is_locked=False)
    door69 = DoorModel(id=69, name="Num69", is_locked=True)
    door50 = DoorModel(id=50, name="Num50", is_locked=False)
    door27 = DoorModel(id=27, name="Num27", is_locked=False)
    door36 = DoorModel(id=36, name="Num36", is_locked=False)
    door33 = DoorModel(id=33, name="Num33", is_locked=False)
    door40 = DoorModel(id=40, name="Num40", is_locked=True)
    door56 = DoorModel(id=56, name="Num56", is_locked=False)
    door79 = DoorModel(id=79, name="Num79", is_locked=True)
    db.session.add_all(
        [
            room1,
            room2,
            room3,
            room4,
            room5,
            room6,
            room7,
            room8,
            room9,
            room10,
            room11,
            room12,
            room13,
            room14,
            room15,
            room16,
            room17,
            room18,
            room19,
            room20,
            room21,
            room22,
            room23,
            door13,
            door22,
            door71,
            door88,
            door17,
            door15,
            door30,
            door50,
            door60,
            door70,
            door99,
            door11,
            door66,
            door42,
            door96,
            door69,
            door27,
            door36,
            door33,
            door40,
            door56,
            door79,
        ]
    )
    db.session.commit()
