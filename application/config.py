import os
from datetime import timedelta

from dotenv import load_dotenv


class Config(object):
    """
    Default Configuration
    """
    load_dotenv()
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_DIR = os.getenv('UPLOAD_DIR')
    SECRET_KEY_USER = os.getenv('SECRET_KEY_USER')


    REDIS_URL = os.getenv('REDIS_URL')
    COMMISION = os.getenv('COMMISION')


    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'port': int(os.getenv('MONGODB_PORT'))
    }

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    INSTALLED_APP_RESOURCES = [
        'user',
        'location',
    ]

    CELERY_TASK_LIST = [
        'utils.util_push_notification',
    ]
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_ACCEPT_CONTENT = ''
    CELERY_TASK_SERIALIZER = ''
    CELERY_RESULT_SERIALIZER = ''
    CELERY_REDIS_MAX_CONECCTIONS = ''

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_HEADER_TYPE = 'JWT'

    IMAGE_ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'svg'}
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'svg'}

    # To enable flask to catch package exceptions
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(Config):
    """
    Development Configuration
    """
    DEBUG = True


class DeploymentConfig(Config):
    """
    Deployment Configuration
    """
    DEBUG = False


class TestingConfig(Config):
    """
        Test Configuration
    """
    DB_SERVER = 'localhost'
    DEBUG = False
    TESTING = True
    MONGODB_SETTINGS = {
        'db': os.getenv('TEST_MONGODB_DB'),
        'host': os.getenv('TEST_MONGODB_HOST'),
        'port': int(os.getenv('TEST_MONGODB_PORT'))
    }
    POSTGRES_USER = os.getenv('TEST_POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('TEST_POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('TEST_POSTGRES_DB')
    POSTGRES_HOST = os.getenv('TEST_POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('TEST_POSTGRES_PORT')
    KAVEH_NEGAR_API_KEY = os.getenv('TEST_KAVEH_NEGAR_API_KEY')
    SECRET_KEY = os.getenv('TEST_SECRET_KEY')
    UPLOAD_DIR = os.getenv('TEST_UPLOAD_DIR')
    SECRET_KEY_USER = os.getenv('TEST_SECRET_KEY_USER')
    PATIENT_REPORTS_IMG_PATH = os.getenv('TEST_PATIENT_REPORTS_IMG_PATH')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
