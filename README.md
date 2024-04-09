# stf-nomic-game

## Installation

### Setting Up Poetry

To install the dependencies for this project, you will need to have Poetry installed. You can install Poetry by running the following command:

```
curl -sSL https://install.python-poetry.org | python3 -
```

### Installing Dependencies

To install the dependencies for this project, run the following command:

```
poetry install
```

### Activating the Virtual Environment

To activate the virtual environment created by Poetry, run the following command:

```
poetry shell
```

### Running the Flask Server

To start the Flask server, run the following command:

```
flask run
```

### Test the API

To test the API, you can use the following command:

```
curl http://localhost:5000/game
```
### Working with the New Directory Structure

The application structure has been updated to include three new directories: `utilities`, `models`, and `routes`. Here's how to work with each:

- `utilities`: Contains utility functions and helpers used across the application. To add a new utility, create a `.py` file within this directory and import it where needed.

- `models`: This directory houses the application's data models. Each model should be defined in its own file, following the SQLAlchemy ORM conventions for Flask.

- `routes`: Contains the route definitions for the application. Each route should be defined in its own file, and imported into the application's main file to be registered.

### Setting Up the `instance` Folder

The `instance` folder is used for instance-specific configurations that shouldn't be committed to version control. To set it up:

1. Create a folder named `instance` at the root of your project.
2. Inside `instance`, create a `config.py` file.
3. Add your instance-specific configurations to `config.py`, such as database URI, secret keys, etc.

Remember to add `/instance` to your `.gitignore` file to prevent committing sensitive information.

