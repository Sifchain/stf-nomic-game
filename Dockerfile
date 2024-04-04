# Use an official Python runtime as a parent image
FROM python:3.8-slim as builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --user -r requirements.txt

# Use a second stage to create a lean production image
FROM python:3.8-slim
COPY --from=builder /root/.local /root/.local
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV PATH=/root/.local:$PATH

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:80", "yourapp:app"]