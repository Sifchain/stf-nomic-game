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

2. Run the command to create the `venv` folder inside the project

```
poetry config virtualenvs.in-project true
```

### Install Docker

1. Install Docker Desktop from the [Docker website](https://docs.docker.com/engine/install/).

### Install Nomic Game

1. Clone this repository:

```
git clone git@github.com:Sifchain/stf-nomic-game.git
```

2. Navigate to the repository folder and install:

```
make init
```

### Configure Nomic Game

1. This project uses a .env file for configuration. To set up your own environment, copy the .env.example file to .env and update the values to match your local setup.

```
cp .env.example .env
```

2. Navigate to the dev branch with the following command:

```
git checkout master
```

### Install the Database

1. Load environment variables

```
source .env
```

2. Start the database container

```
make start-db
```

3. Migrate the database

```
make migrate-db
```

### Running the API Server

To start the API server, run the following command:

```
python -m nomic.main
```

### Test the API

To test the API, you can open the swagger UI:

http://localhost:8000
