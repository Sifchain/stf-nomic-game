class BaseConfig:
    # Basic configuration applicable to all environments
    DEBUG = False
    SECRET_KEY = 'your_secret_key'
    DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    # Development specific configurations
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(BaseConfig):
    # Production specific configurations
    DEBUG = False
    DATABASE_URI = 'sqlite:///prod.db'
    SECRET_KEY = 'your_production_secret_key'
    # Add more secure settings here
