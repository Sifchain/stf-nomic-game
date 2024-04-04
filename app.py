from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CSRFProtect(app)
limiter = Limiter(app, key_func=get_remote_address)
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to our Flask app!'
@app.route('/start_game')
def start_game():
    return 'Starting a new game!'

@app.route('/join_game')
def join_game():
    return 'Joining a game!'

@app.route('/take_turn')
def take_turn():
    return 'Taking a turn in the game!'
if __name__ == '__main__':
    app.run(debug=True)