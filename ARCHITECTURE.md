# Server Architecture

## Overview

The `stf-nomic-game` project is a FastAPI-based web application designed to facilitate online Nomic games—a game where the rules evolve as players make decisions. This document outlines the architectural components of the server, including the API services, database models, WebSocket communication, and security features.

## Technologies

- **FastAPI**: Web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Uvicorn**: ASGI server for running FastAPI applications.
- **SQLAlchemy**: SQL toolkit and ORM for database interactions.
- **Alembic**: Database migrations tool that utilizes SQLAlchemy.
- **Poetry**: Dependency management and packaging tool.
- **Docker**: Platform for developing, shipping, and running applications.
- **JWT (JSON Web Tokens)**: Method for securely transmitting information between parties as a JSON object.

## Project Structure

```
/stf-nomic-game
|-- alembic/                     # Database migrations scripts and configurations
|-- nomic/                       # Main application package
|   |-- database/                # Database models, CRUD operations setup
|   |-- routes/                  # API routes definitions
|   |-- services/                # Business logic layer
|   |-- utils/                   # Utility functions including security and JWT handlers
|   `-- main.py                  # Entry point for the FastAPI application
|-- tests/                       # Test scripts for the application
|-- pyproject.toml               # Project metadata and dependencies managed by Poetry
|-- README.md                    # Project overview and setup instructions
|-- .env                         # Environment variables configuration
|-- Dockerfile                   # Instructions for Docker to build the application
`-- scripts/                     # Additional scripts, e.g., for WebSocket testing
```

## API Components

### Core API

- **FastAPI Application Setup**: Configured in `nomic/main.py` with CORS middleware, routes inclusion, and startup settings.
- **CORS Middleware**: Allows or restricts resources on a web page from requesting resources from another domain.

### Routes

- **Home Route**: Basic route for server root access.
- **Authentication Routes**: Includes user registration, login, and token validation.
- **Game Management Routes**: Handling game creation, joining, rule submission, and voting via API and WebSocket.

### WebSocket

- Managed in `nomic/routes/ws.py`, it handles real-time communication for game events.
- **WebSocket Route**: `/ws` for accepting connections and broadcasting game updates.

## Database Setup

- **SQLAlchemy ORM**: Used for defining database models and performing database operations.
- **Alembic**: Manages schema migrations.
- **Models**: Defined in `nomic/database/models.py`, starting with a `User` model.
- **CRUD Operations**: Standard create, read, update, and delete operations are managed in `nomic/database/crud.py`.

## Security

- **Passlib**: Library for password hashing.
- **JWT**: Used for generating and verifying tokens to handle authentication and authorization.
- **OAuth2**: Security protocol for token management in HTTP services.

## Development and Deployment

- **Poetry**: Manages dependencies and virtual environments.
- **Docker**: Used to containerize the application for consistent deployment environments.
- **Alembic**: For handling database migrations.

## Testing

- **Pytest**: For writing and running tests.
- **Test Coverage**: Includes API endpoints and WebSocket connections.

## Setup and Installation

Detailed setup and installation instructions are available in `README.md`, covering environment setup, dependency installation, and running the application.

## Future Considerations

- Integrating more sophisticated user and session management.
- Expanding the database schema to support advanced game mechanics.
- Enhancing WebSocket functionality for better real-time interactions.
