import os

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///dev.db')

class ProductionConfig(BaseConfig):
    DEBUG = False
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI', 'sqlite:///prod.db')
