import pytest
import os
import json
from flask_jwt_extended import create_access_token
from application.app import create_app
from application.extensions import db, redis_client
from manage import create_db
import seeder_constant_test
import seeder_constant
from models import *
from mongoengine.connection import disconnect_all


"""
 In this fixture creates the test client using a context manager
 and then the application context is pushed onto the stack for use by the test functions
 The yield testing_client statement means that execution is being passed to the test functions.
"""


@pytest.fixture(scope='module')
def client():
    disconnect_all()
    flask_app = create_app('application.config.TestingConfig')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context() as app_context:
            db.drop_all()
            UserProgramReport.objects().delete()
            db.create_all()
            seed_test_db(flask_app)
            yield testing_client  # this is where the testing happens!


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    flask_app = create_app('application.config.TestingConfig')
    with flask_app.app_context():
        db.drop_all()
        UserProgramReport.objects().delete()


@pytest.fixture(scope='module')
def get_user_token():
    user = User.query.filter_by(mobile="+989125486997").first()
    return create_access_token(identity=user.id, )


def seed_test_db(flask_app):
    for list_name in dir(seeder_constant_test):
        if list_name.startswith("M"):
            model_name = list_name.split("_")[1]
            list_instance = getattr(seeder_constant_test, list_name)

            obj = eval(model_name)(**record)
            db.session.add(obj)
            db.session.commit()


def seed_redis(app):
    try:
        with app.app_context():
            redis_client.set(key, value)
    except:
        print("redis database not seeded yet or not connected to redis")
