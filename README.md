# stf-nomic-game

## Setup Instructions

### Flask Application Setup
1. Ensure Python 3.8+ is installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the cloned repository and create a virtual environment:
   - `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Unix or MacOS: `source venv/bin/activate`
5. Install the required dependencies:
   - `pip install -r requirements.txt`
6. Start the Flask application:
   - `flask run`

### Environment Configuration
- Copy the `.env.example` file to `.env` and modify it according to your local environment settings.

### Docker Containerization
1. Ensure Docker is installed on your system.
2. Build the Docker image:
   - `docker build -t stf-nomic-game .`
3. Run the Docker container:
   - `docker run -d -p 5000:5000 stf-nomic-game`

## Contribution Guidelines

### Coding Standards
- Follow PEP 8 for Python code.
- Ensure code is well-commented and adheres to project structure.

### Branch Naming Conventions
- Use descriptive branch names, prefixed with the type of work being done (`feat/`, `fix/`, `docs/`, etc.).

### Pull Request Process
- Ensure your code passes all tests and adheres to coding standards.
- Provide a detailed description of the changes in the pull request.
- Request a review from a project maintainer.