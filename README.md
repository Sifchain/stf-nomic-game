# stf-nomic-game

## Setup Instructions

### Flask Application Setup
1. Ensure Python 3.8+ is installed on your system.
2. Install Flask using pip: `pip install Flask`.
3. Navigate to the project directory and run the application: `flask run`.

### Environment Configuration
1. Copy `.env.example` to `.env` and modify the variables to fit your environment.
2. Ensure all required environment variables are set before starting the application.

### Docker Containerization
1. Ensure Docker is installed on your system.
2. Build the Docker image: `docker build -t stf-nomic-game .`.
3. Run the container: `docker run -d -p 5000:5000 stf-nomic-game`.

## Contribution Guidelines

### Coding Standards
- Follow PEP 8 for Python code.
- Ensure code is well-commented and adheres to the project's architectural design.

### Branch Naming Conventions
- Feature branches should be named `feature/<feature-name>`.
- Bugfix branches should be named `bugfix/<bug-name>`.
- Documentation updates should be named `docs/<documentation-name>`.

### Pull Request Process
1. Ensure your code passes all tests and adheres to the coding standards.
2. Update the README.md if necessary.
3. Submit a pull request to the `main` branch.
4. The pull request must be reviewed and approved by at least one project maintainer.