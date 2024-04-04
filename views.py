from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Nomic game! Stay tuned for more updates.'

@app.route('/game')
def game():
    return 'Game session will be available soon. Exciting functionalities are coming!'

if __name__ == '__main__':
    app.run(debug=True)