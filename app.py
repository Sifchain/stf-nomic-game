from flask import Flask

app = Flask(__name__)

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