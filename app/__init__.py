from flask import Flask
import os

app = Flask(__name__, instance_relative_config=True)
# app.config.from_object('config')

from .routes import *