from . import app

@app.route('/')
def home():
    return '<h1>Welcome to the Nomic Game!</h1><p>Embark on a journey where the rules of the game are decided by the players themselves.</p>'

@app.route('/game')
def game():
    return '<h1>Game functionalities coming soon!</h1>'