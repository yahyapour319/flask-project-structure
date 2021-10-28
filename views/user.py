from flask import Blueprint,request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from marshmallow import ValidationError
from datetime import datetime

from models.user import User
from models.errors_enum import ErrorEnum
from schemas.user import UserSchema
from application.extensions import db
from flask_restful import Resource, Api


class AppUser(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        return UserSchema(only=("full_name", "mobile", "city", "national_id", "gender")).dump(user)

    @jwt_required
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = UserSchema(
                only=("id", "user_info", "user_info", "about_us", "birthdate", "city_id",
                    "other_fields ...")).load(request.json, instance=User.query.get_or_404(user_id), partial=True)
            user.user_info.updated_at = datetime.utcnow()
            db.session.commit()
        except ValidationError as err:
            return {"error_msg"=err.messages} , 422

        return {'user_id':user.id}


def get_resources():
    """
    Returns app user resources.
    :param app: The Flask instance
    :return: App user resources
    """
    blueprint = Blueprint('app_user', __name__, url_prefix='/api/v1')
    api = Api(blueprint)

    api.add_resource(AppUser, '/user')

    return blueprint
