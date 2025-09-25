import threading, pathlib, logging

from datetime import timedelta
from flask import Flask
from waitress import serve
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler

import thread_check

from api_resources import (
    welcome_blp,
    login_blp,
    frontdoor_blp,
    doors_blp,
    uploads_blp,
    rooms_blp,
    hearts_blp,
)
from database import db, init_db
from log import AppLogger

scheduler: APScheduler = APScheduler()


class FlaskApp:
    def __init__(self, name=__name__, config=None):
        self.app = Flask(name)
        scheduler.init_app(self.app)
        scheduler.start()
        if config:
            self.app.config.from_object(config)
        jwt = JWTManager(self.app)
        self.app.register_blueprint(welcome_blp)
        self.app.register_blueprint(login_blp)
        self.app.register_blueprint(frontdoor_blp)
        self.app.register_blueprint(doors_blp)
        self.app.register_blueprint(uploads_blp)
        self.app.register_blueprint(rooms_blp)
        self.app.register_blueprint(hearts_blp)
        db.init_app(self.app)
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            init_db()

    def start_thread(self):
        threading.Thread(
            target=thread_check.check_tokens, args=(self.app,), daemon=True
        ).start()


class DevLauncher(FlaskApp):
    def __init__(self):
        super().__init__(config=DevConfig)
        scheduler.add_job(
            id="archive_dev_logs",
            func=AppLogger.archive_logs,
            args=("dev",),
            trigger="interval",
            seconds=15,
            max_instances=1,
        )

    def run(self):
        self.start_thread()
        AppLogger.set_up_logger(
            filename=pathlib.Path("./log") / "devlog.txt", level=logging.DEBUG
        )
        self.app.run(use_reloader=False)


class ProdLauncher(FlaskApp):
    def __init__(self):
        super().__init__(config=ProdConfig)

    def run(self):
        self.start_thread()
        logged_app = AppLogger.set_up_translogger(app=self.app)
        AppLogger.set_up_logger(
            filename=pathlib.Path("./log") / "log.txt", level=logging.INFO
        )
        serve(app=logged_app, listen="0.0.0.0:5050")


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    JWT_SECRET_KEY = "veryspecialsupersecretkey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=10)


class DevConfig(FlaskConfig):
    DEBUG = True


class ProdConfig(FlaskConfig):
    DEBUG = False
