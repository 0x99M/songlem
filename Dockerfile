# Use official Python 3 image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations, seed data, and start the server
CMD ["bash", "-c", "python3 manage.py migrate && python3 manage.py seed && gunicorn songlem.wsgi:application --bind 0.0.0.0:8000"]
