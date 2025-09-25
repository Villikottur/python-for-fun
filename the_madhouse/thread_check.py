import time, logging
from flask import Flask
from flask_restful import abort
from flask_jwt_extended import decode_token
from flask_jwt_extended.jwt_manager import ExpiredSignatureError
from sqlalchemy.exc import SQLAlchemyError
from database import db
from db_models import UserModel, TokenModel


def check_tokens(flask_app: Flask):
    while True:
        with flask_app.app_context():
            live_users = (
                db.session.query(UserModel).filter(UserModel.is_alive == True).all()
            )
            usernames = [user.username for user in live_users]
            tokens = (
                db.session.query(TokenModel)
                .filter(TokenModel.username.in_(usernames))
                .all()
            )
            try:
                for token in tokens:
                    for user in live_users:
                        if user.hearts < 1:
                            user.is_alive = False
                            user.current_room = None
                            token.is_expired = True
                        if user.username == token.username:
                            try:
                                decode_token(token.token)
                                token.is_expired = False
                                user.is_alive = True
                            except ExpiredSignatureError as e:
                                token.is_expired = True
                                user.is_alive = False
                                user.current_room = None
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(
                    500,
                    message="Unexpected database error (thread).",
                )
            db.session.commit()
            newly_live_users = (
                db.session.query(UserModel).filter(UserModel.is_alive == True).count()
            )
            logging.log(
                level=logging.INFO,
                msg=f"There are currently {newly_live_users} players that are still alive.",
            )
        time.sleep(30)
