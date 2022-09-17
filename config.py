import os


# Задаем секретный ключ
class BaseConfig:
    SECRET_KEY = "sdfksdfh6lks2jklb3nksd"
    BOOTSTRAP_SERVE_LOCAL = True
    DEBUG = False


# Конфиг для среды разработки? ,будет использована по умолчанию
class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                              'mysql+pymysql://root:pass@localhost/flask_app_db'


# Конфиг для среды тестирования сервера
class TestConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
                              'mysql+pymysql://root:pass@localhost/flask_app_db'


# Конфиг продакшена
class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'mysql+pymysql://root:pass@localhost/flask_app_db'
