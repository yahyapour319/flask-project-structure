import json

from flask import current_app
from flask_migrate import MigrateCommand
from flask_script import Manager

from application.app import create_app
from application.extensions import db, redis_client
from models import *
import seeder_constant

app = create_app('application.config.DeploymentConfig')
manager = Manager(app)

manager.add_command('db', MigrateCommand)

'''
    AT THIS FILE :
        Implement methods which is commonly 
        use in development befor start a project
'''


@manager.command
def create_db():
    '''
        Creates database base on defined models
    '''
    db.create_all()


@manager.command
def drop_db():
    '''
        Drops Database.
    '''
    db.drop_all()


@manager.command
def drop_collection_mongo(CollectionName):
    '''
         delete mongo documents in a Collection
         use flask_mongoengine.MongoEngine
    '''
    eval(CollectionName)().objects().delete()


@manager.command
def del_object(class_name, id):
    '''
        for deleting specific row(object)
        Command Example: python3 manage.py del_object ModelName id
    '''
    try:
        eval(class_name)().query.get(id).delete()
    except Exception as err:
        print(str(err))


@manager.command
def seed_db():
    '''
        Fill database by predefined recoreds, which
        is defined in seed file, for deployment or test.
        models in seed file are defined like:
            M[no]_ModelName (ex: M25_Doctor or M24_UserInfo)
    '''

    for list_name in dir(seeder_constant):
        if list_name.startswith("M"):
            model_name = list_name.split("_")[1]
            list_instance = getattr(seeder_constant, list_name)
            for record in list_instance:
                obj = eval(model_name)(**record)
                db.session.add(obj)
                db.session.commit()


@manager.command
def seed_redis():
    '''
        Fill Redis by :
            Pre-defined data(key value),
            which is cached in redis to improve performance 
    '''
    try:
        with app.app_context():
            redis_client.set('foo', 'bar')
    except:
        print("redis database not seeded yet or not connected to redis")


if __name__ == '__main__':
    manager.run()
