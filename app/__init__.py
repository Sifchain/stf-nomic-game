from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config.' + os.getenv('FLASK_ENV', 'DevelopmentConfig'))

from .routes import *