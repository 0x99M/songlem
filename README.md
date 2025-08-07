# Songlem - Music Catalog API

Songlem is a Django-based application for managing a music library catalog, including artists, albums, and songs. It provides a clear data structure and includes a powerful seeding command to populate the database with realistic fake data for development and testing purposes.

## Features

*   **Data Models**: Well-defined Django models for `Artist`, `Album`, and `Song` with many-to-many relationships.
*   **Database Seeding**: A custom management command (`seed`) to quickly populate the database.
*   **Performance**: The seeding script is optimized using `bulk_create` to handle large amounts of data efficiently.
*   **Customizable Seeding**: Control the amount of data to generate and optionally preserve existing data.

## Requirements

*   Python 3.8+
*   Django
*   graphene-django
*   django-cors-headers
*   Faker
*   Gunicorn

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd songlem
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    This will create the necessary tables in your database based on the models in `core/models.py`.
    ```bash
    python3 manage.py migrate
    ```

## Usage with Docker Compose (Recommended)

This project is configured to run with Docker Compose. This is the recommended way to run the application for development and testing, as it uses a self-contained SQLite database.

### Prerequisites

*   Docker
*   Docker Compose

### Running the Application

1.  **Build and start the service:**
    This command will build the Docker image and start the web service container in the background.
    ```bash
    docker-compose up --build -d
    ```

2.  **Apply database migrations:**
    Run the `migrate` command inside the container to set up your SQLite database schema.
    ```bash
    docker-compose exec web python manage.py migrate
    ```

3.  **Seed the database:**
    To populate the database with fake data, run the `seed` command.
    ```bash
    docker-compose exec web python manage.py seed
    ```
    You can now access the application at `http://12-7.0.0.1:8000`.

### Daily Usage

*   **Start the services:** `docker-compose up -d`
*   **Stop the services:** `docker-compose down`
*   **View logs:** `docker-compose logs -f web`
*   **Run any management command:** `docker-compose exec web python manage.py <command>`