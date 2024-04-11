from flask import Flask
from .models import db

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

# set db to use the app
db.init_app(app)

# apply the routes to the app
from .routes import *