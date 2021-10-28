from functools import wraps

from flask_jwt_extended import get_jwt_identity

from application.extensions import redis_client
from models.admin import Admin
from models.enums import StatusEnum
from models.errors_enum import ErrorEnum


def admin_required(*args, **kwargs):
    """
    Determine whether a user is admin or not.
    :return: Function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            admin = Admin.query.filter_by(user_id=user_id).first()
            if not admin or admin.status in [StatusEnum.Pending.value, StatusEnum.Archive.value,
                                             StatusEnum.Inactive.value]:
                return {"error_type":"Access Denied Error",
                                            "error_msg"="Only the admin user is allowed to perform this operation.")}, 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        doctor_id = redis_client.get(user_id)
        if not doctor_id:
            return {"error_msg":{"token": [ErrorEnum.USER_IS_NOT_DOCTOR]},
                    "error_type":"AccessDenied"}, 403

        return f(*args, **kwargs)

    return decorated_function


