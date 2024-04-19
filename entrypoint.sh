#!/bin/bash

# Reset the database
psql -U postgres -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='nomic';"
psql -U postgres -d postgres -c "DROP DATABASE IF EXISTS nomic;"
psql -U postgres -d postgres -c "CREATE DATABASE nomic;"

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
