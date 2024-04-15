#!/bin/bash

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
