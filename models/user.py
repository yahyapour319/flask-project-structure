import re
from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy.util import timezone

from application.extensions import db
from models.city import City
from utils.util_sqlalchemy import ModelMixin


class User(ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    email = db.Column(db.String, unique=True)
    about_us = db.Column(db.String)
    avatar = db.Column(db.String)
    birthdate = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))



    @validates('national_id')
    def validate_national_id(self, key, national_id):
        if national_id:
            regex = re.compile(r"^\d{10}$")
            assert regex.match(national_id), "national_id"
        return national_id

    @validates('mobile')
    def validate_mobile(self, key, mobile):
        regex = re.compile(r"^9\d{9}$")
        assert regex.match(mobile), "mobile"
        return mobile

    @validates('email')
    def validate_email(self, key, email):
        if email:
            regex = re.compile(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{1,3})$")
            assert regex.match(email), "email"
        return email

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or mobile number.

        :param identity: Email or mobile
        :type identity: str
        :return: User instance
        """

        return cls.query.filter((cls.email == identity) | (cls.mobile == identity)).first()

    @classmethod
    def find(cls, **kwargs):
        """
         Find a User.
         return: User instance
         """
        q = cls.query
        for attr, value in kwargs.items():
            q = q.filter(getattr(cls, attr) == value)
        return q.first()

    @classmethod
    def create_user(cls, **kwargs):
        user = cls(**kwargs).update_or_create()
        return user
