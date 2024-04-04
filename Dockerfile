# Start with a Python image
FROM python:3.8-slim as builder

# Set a working directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Multi-stage to slim down the image size
FROM python:3.8-slim

WORKDIR /usr/src/app

# Copy only the dependencies installation from the 1st stage image
COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/src/app /usr/src/app

# Set the environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 8000

# Install Gunicorn
RUN pip install gunicorn

# Run Gunicorn with one worker
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]