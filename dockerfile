# Use an official lightweight Python image.
FROM python:3.11-slim

# Set environment variables for the container.
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy requirements first to leverage Docker cache.
COPY requirements.txt .

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Tell the container to run the Gunicorn server, listening on port 8080.
# This command starts our web app.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
