import importlib
import json
import os

from celery import Celery
from flask import Flask, request
from marshmallow import ValidationError
from application.extensions import db, ma, migrate, jwt, mongo, redis_client


def create_app(config_filename):
    # __name__ : current Python module
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_filename)
    if not app.config['TESTING']:
        app.response_class = CustomResponse

    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)
    redis_client.init_app(app, charset="utf-8", decode_responses=True)


    for installed_app_resources in app.config['INSTALLED_APP_RESOURCES']:
        app_resource = importlib.import_module(f'views.{installed_app_resources}')
        app.register_blueprint(app_resource.get_resources())

    # CREATE STATIC FOLDER:
    static_folder_path = app.config['UPLOAD_DIR']
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)

    return app


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=app.config['CELERY_TASK_LIST'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
