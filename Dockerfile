FROM python:3.9.5-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.in
RUN pip install --no-cache-dir -r requirements.in

# Set the environment variable for Celery
ENV DJANGO_SETTINGS_MODULE=playlist_ninja.settings

# Expose port 8000 for the Django app
EXPOSE 8000

# Start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]