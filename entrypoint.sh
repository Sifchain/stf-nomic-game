#!/bin/bash

# Create database if not exists
psql postgresql://postgres:postgres@nomic-db:5432/postgres -c "SELECT 1 FROM pg_database WHERE datname='nomic'" | grep -q 1 || psql postgresql://postgres:postgres@nomic-db:5432/postgres -c "CREATE DATABASE nomic;"

# Run Alembic migrations
echo "Running Alembic migrations..."
python ./migration.py

# Check if migration was successful
if [ $? -ne 0 ]; then
    echo "Migration failed, exiting."
    exit 1
fi

# Start the main application
echo "Starting main application..."
exec python -m nomic.main
