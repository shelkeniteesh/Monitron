# Use an official Python runtime as a parent image
# Choose a Python version that matches your project. Python 3.11-slim is a good default.
FROM python:3.11-slim

# Set environment variables for Python
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1  
# Ensures Python output is sent straight to terminal (good for logging)
ENV PYTHONUNBUFFERED=1        
# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
# Uncomment and add your dependencies if needed (e.g., for psycopg2, Pillow).
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group for security
RUN addgroup --system app && adduser --system --ingroup app app

# Install Python dependencies
# Copying requirements.txt first leverages Docker's layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Collect static files
# Ensure STATIC_ROOT is correctly set in your Django settings.py.
# The --clear option removes any stale files from previous collections.
# RUN python manage.py collectstatic --noinput --clear

# Change ownership of the app directory and its contents to the non-root user
# This includes the collected static files.
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Gunicorn will run on.
# Cloud Run automatically provides the PORT environment variable (default 8080).
EXPOSE 8080

# Command to run the application using Gunicorn
# Replace 'your_project_name' with the actual name of your Django project
# (the directory containing your wsgi.py file).
# Gunicorn will bind to 0.0.0.0 and the port specified by the PORT env variable.
# The number of workers (e.g., 3) can be tuned. A common starting point is (2 * CPU_CORES) + 1.
# Cloud Run default instances often have 1 vCPU.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "monitron.wsgi:application"]