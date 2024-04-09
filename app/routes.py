from . import app

@app.route('/')
def home():
    return '<h1>Welcome to the Nomic Game!</h1><p>Embark on a journey where the rules of the game are decided by the players themselves.</p>'
