from marshmallow import fields, post_dump, validates_schema, ValidationError

from application.extensions import ma
from models.user import User
from models.user_info import UserInfo
from marshmallow.validate import Regexp
from models.location import City, Province
from models.errors_enum import ErrorEnum
from schemas.location import CitySchema


class UserInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserInfo
        include_fk = True
        load_instance = True
        include_relationships = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    city = ma.Nested(CitySchema())
    created_at = fields.DateTime(format='%Y/%m/%d-%H:%M')
    user_info = ma.Nested(UserInfoSchema())
    mobile = fields.String(required=True, validate=[Regexp(r"^(9|09)\d{9}$")])

    class Meta:
        model = User
        exclude = ['updated_at']
        include_fk = True
        include_relationships = True
        load_instance = True

    @validates_schema
    def validate_location(self, data, **kwargs):
        if not 'city_id' in data:
            raise ValidationError({"city_id": ErrorEnum.INVALID_CITY})

    @post_dump
    def show_mobile_with_country_code(self, data, **kwargs):
        if 'country' in data and 'mobile' in data:
            data['mobile'] = data['country']['dial_code'] + data['mobile']
            del data['country']
        return data


specific_user_schema = UserSchema(only=("full_name", "national_id", "gender",
                                        "country_id", "city_id", "email", "birthdate",
                                        "avatar", "is_doctor", "user_info"))
user_schema = UserSchema()
