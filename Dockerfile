# Use official Python 3 image
FROM python:3.11-slim

# Recommended environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Default command: run migrations, seed the DB, then launch the app
CMD bash -c "
  python3 manage.py migrate &&
  python3 manage.py seed &&
  gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
"
