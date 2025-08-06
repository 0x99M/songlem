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
*   Faker

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

## Usage

### Seeding the Database

The project includes a command to populate your database with fake data. This is extremely useful for development and testing.

**Basic usage (uses default values):**
```bash
python3 manage.py seed
```

**Customizing the data volume:**
You can specify the number of artists, albums, and songs per album.
```bash
python3 manage.py seed --artists 50 --albums 100 --songs-per-album 15
```

**Appending data without deleting existing records:**
Use the `--no-clean` flag to add more data to the database without clearing it first.
```bash
python3 manage.py seed --no-clean
```

### Running the Development Server

To start the Django development server, run:
```bash
python3 manage.py runserver
```

You can now access the application at `http://127.0.0.1:8000`.