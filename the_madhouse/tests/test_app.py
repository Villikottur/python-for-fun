import unittest, io

from flask_testing import TestCase
from flask_jwt_extended import create_access_token, create_refresh_token

from app import DevLauncher, scheduler
from database import db
from db_models import UserModel, RoomModel, DoorModel, TokenModel


class MyTest(TestCase):
    def create_app(self):
        self.app = DevLauncher().app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        self.app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        with self.app.app_context():
            scheduler.shutdown(wait=False)
        return self.app

    def setUp(self):
        with self.app.app_context():
            db.create_all()
        door = DoorModel(id="666", name="testdoor", is_locked=True)
        if not DoorModel.query.filter_by(id="666", is_locked=True).first():
            db.session.add(door)
            db.session.commit()
        if not RoomModel.query.filter_by(name="first_room").first():
            db.session.add_all(
                [
                    RoomModel(
                        name="first_room",
                        items="key,heart",
                        south_exit=door,
                    ),
                    RoomModel(name="entrance_hall", north_exit=door),
                ]
            )
            db.session.commit()
        test_user = UserModel(
            username="testuser",
            password="778dfbnhd",
            items="heart",
            current_room="first_room",
        )
        db.session.add(test_user)
        db.session.commit()
        self.token = create_access_token(identity={"username": "testuser"}, fresh=True)
        self.refresh_token = create_refresh_token(identity={"username": "testuser"})
        db.session.add(TokenModel(username="testuser", token=self.token))
        db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_api_hearts(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(path="/hearts", headers=headers)
        self.assert200(response=response)

    def test_api_home(self):
        response = self.client.get(path="/")
        self.assert200(response=response)
        json_data = {"knocks": 6, "username": "df98jsd", "password": "f9s8jf"}
        response = self.client.post(path="/frontdoor", json=json_data)
        self.assertStatus(response=response, status_code=201)

    def test_api_frontdoor(self):
        json_data = {"username": "test", "password": "f9s8jf", "knocks": 6}
        response = self.client.post(path="/frontdoor", json=json_data)

    def test_api_dooors(self):
        json_data = [
            {"name": "bl4f4la", "id": 3},
            {"name": "blabl4rtffbla", "id": 7163},
        ]
        response = self.client.post(path="/doors", json=json_data)
        self.assertStatus(response=response, status_code=201)

    def test_api_get_room(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(path="/room/first_room", headers=headers)
        self.assert400(response=response)

    def test_api_entrancehall(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(path="/room/begin/entrance_hall", headers=headers)
        self.assert200(response=response)

    def test_api_drop(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        json_data = {"items": "key"}
        response = self.client.put(
            path="/room/first_room/drop", headers=headers, json=json_data
        )
        self.assert200(response=response)

    def test_api_roomlights(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(path="/room/first_room/lights", headers=headers)
        self.assert200(response=response)

    def test_api_room(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        json_data = {"items": "key"}
        response = self.client.put(
            path="/room/first_room/pick_up", headers=headers, json=json_data
        )
        self.assert200(response=response)

        response = self.client.put(path="/room/first_room/666/key", headers=headers)
        self.assert200(response=response)

        response = self.client.put(path="/room/first_room/666/open", headers=headers)
        self.assert200(response=response)
        response = self.client.get(path="/room/first_room/666", headers=headers)
        self.assert200(response=response)

        headers = {"Authorization": f"Bearer {self.refresh_token}"}
        response = self.client.post(path="/login/restart", headers=headers)
        self.assertStatus(response=response, status_code=201)

    def test_api_upload(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"file": (io.BytesIO(b"Just a test"), "testfile.txt")}
        response = self.client.post(
            path="/upload",
            data=data,
            content_type="multipart/form-data",
            headers=headers,
        )
        self.assert200(response=response)


if __name__ == "__main__":
    unittest.main()
