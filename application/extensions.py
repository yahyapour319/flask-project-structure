from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
mongo = MongoEngine()
redis_client = FlaskRedis()

cors = CORS(resources={r"/api/*": {"origins": "*"}})


