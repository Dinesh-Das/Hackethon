# Dockerfile

# Use an official Python runtime as a parent image (slim version is lightweight)
FROM python:3.11-slim

# Set environment variables for the container
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME

# Install system dependencies that might be needed by Python packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker's build cache.
# This layer is only rebuilt when requirements.txt changes.
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your app using Gunicorn.
# gunicorn is a production-ready WSGI server.
# --bind 0.0.0.0:$PORT makes the app accessible from outside the container.
# main:app tells Gunicorn to look for an object named 'app' in a file named 'main.py'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
