from flask import Flask

app = Flask(__name__)

# Import routes from views
from views import *

if __name__ == '__main__':
    app.run(debug=True)