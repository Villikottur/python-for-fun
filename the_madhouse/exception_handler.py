from functools import wraps
from flask_restful import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow.exceptions import MarshmallowError, ValidationError
from flask_jwt_extended.jwt_manager import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError
from database import db


def handle_exceptions(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NoAuthorizationError as e:
                abort(
                    400,
                    message="You need a token to access this endpoint. Go to /login and try again.",
                )
            except ExpiredSignatureError as e:
                abort(
                    400,
                    message="Your token has expired. Which means you're currently DEAD."
                    "If you wanna try again, go to login/restart.",
                )
            except TypeError as e:
                db.session.rollback()
                abort(400, message="Violated database rules.", reason=str(e))
            except IntegrityError as e:
                db.session.rollback()
                abort(400, message="Violated database rules.", reason=str(e.orig))
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(
                    500,
                    message="Unexpected error. Please check your data and try again later.",
                )
            except ValidationError as e:
                for key, value in e.messages.items():
                    if isinstance(value, dict):
                        for sub_key in value.keys():
                            if sub_key in schema.fields:
                                abort(
                                    400,
                                    message=f"Bad request.",
                                    reason=f"Please provide a valid {sub_key}.",
                                )
                            else:
                                abort(
                                    400,
                                    message=f"Bad request.",
                                    reason=f"Please provide valid data.",
                                )
                    elif key in schema.fields:
                        abort(
                            400,
                            message=f"Bad request.",
                            reason=f"Please provide a valid {key}.",
                        )
                    else:
                        abort(
                            400,
                            message=f"Bad request.",
                            reason=f"Please provide valid data.",
                        )
            except MarshmallowError as e:
                abort(400, message="Provided unvalid data.", reason=str(e))

        return wrapper

    return decorator
