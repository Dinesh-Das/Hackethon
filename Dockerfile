# Use an official lightweight Python image.
# FROM python:3.11-slim

# Set environment variables for the container.
# ENV PYTHONUNBUFFERED True
# ENV APP_HOME /app
# WORKDIR $APP_HOME

# Copy requirements first to leverage Docker cache.
# COPY requirements.txt .

# Install production dependencies.
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
# COPY . .

# Tell the container to run the Gunicorn server, listening on port 8080.
# This command starts our web app.
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]



# Use the official Nginx image from Docker Hub. 'alpine' is a lightweight version.
FROM nginx:alpine

# The Nginx image by default looks for files to serve in this directory.
# We set it as our working directory.
WORKDIR /usr/share/nginx/html

# The base Nginx image has its own default welcome page. Let's remove it.
RUN rm index.html

# Copy your local index.html file into the container's web root directory.
# The '.' means "copy the file to the current WORKDIR".
COPY index.html .

# You don't need a CMD or EXPOSE. The base Nginx image already configures
# a command to start the server and exposes port 80.
