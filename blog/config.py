import os

from dotenv import load_dotenv, find_dotenv
from flask import Config

load_dotenv(find_dotenv())  # загрузка пары ключ-значение из файла ".env" для установки переменных окружения
# environment: BaseConfig, DevConfig, TestConfig. Если отсутствует - BaseConfig
CONFIG_NAME = 'DevConfig'


class BaseConfig:
    """ Environment Production """
    FLASK_DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # максимальный размер файла для загрузки на сервер [16M]
    UPLOAD_FOLDER = 'static/storage'
    FLASK_ADMIN_SWATCH = 'Materia'
    FLASK_ADMIN_FLUID_LAYOUT = False


class DevConfig(BaseConfig):
    """ Environment Development """
    FLASK_DEBUG = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class TestConfig(BaseConfig):
    """ Environment Testing """
    TESTING = True


