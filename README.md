# stf-nomic-game
## Setting Up a Python Virtual Environment
To create a new Python virtual environment, run the following command in your terminal:
```
python3 -m venv venv
```

### Activating the Virtual Environment
- On Unix/macOS, activate the environment with:
```
source venv/bin/activate
```
- On Windows, activate the environment using:
```
venv\Scripts\activate
```
### Installing Dependencies
After activating the virtual environment, install the required dependencies by running:
```
pip install -r requirements.txt
```

### Running the Flask Server
To start the Flask server, run the following command:
```
flask run
```

## Integration of Nomic Game Logic into Flask App
To integrate the Nomic game logic into our Flask application, we will follow these steps and make necessary modifications in specific areas of the code:

### Step 1: Define Game Models
- Define models for the game state, rules, and players in `models.py`.

### Step 2: Game Logic API
- Implement an API in `app.py` that handles game actions. This will involve creating routes for starting a game, making moves, and querying the current game state.

### Step 3: Database Integration
- Modify `models.py` to ensure that game states and rules are persistently stored in the database.

### Step 4: User Interface
- Update templates in the `templates` directory to include user interfaces for game interaction.

### Step 5: WebSocket for Real-Time Updates
- Integrate WebSocket in `app.py` for real-time game state updates to all players.

These steps will ensure a seamless integration of the Nomic game logic into our Flask application, providing an interactive and engaging user experience.