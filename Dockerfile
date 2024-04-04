# Use an official Python runtime as a parent image
FROM python:3.8-slim as builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --user -r requirements.txt

# Use a smaller image to run the application
FROM python:3.8-slim
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app /usr/src/app
COPY --from=builder /root/.local /root/.local

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PATH=/root/.local:$PATH

# Run gunicorn when the container launches
CMD ["gunicorn", "-b", ":8000", "app:app"]