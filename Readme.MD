# A service for displaying the current dollar-ruble exchange rate

## Technologies Used

*   Python 3.9
*   Django 4.2
*   Django REST Framework
*   Celery (for asynchronous tasks)
*   Redis (for Celery broker and result backend)
*   PostgreSQL (database)
*   Docker
*   Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed:

*   Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)
*   Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/vorpavnik/currency_test_work
    cd currency
    ```

2.  **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

    This command will:

    *   Build the Docker images for the web, Celery worker, Celery beat, Redis, and PostgreSQL services.
    *   Start all the containers in detached mode.

3.  **Apply database migrations:**

    Open a new terminal and execute the following command to apply the database migrations:

    ```bash
    docker-compose exec currency_web_1 python manage.py migrate
    ```

4.  **Create a superuser (optional):**

    If you want to access the Django admin panel, create a superuser:

    ```bash
    docker-compose exec currency_web_1 python manage.py createsuperuser
    docker-compose exec currency_web_1 python manage.py drf_create_token # for auth from token
    ```

5.  **Access the API:**

    The API will be available at `http://localhost:8000`.

## Notes

*   The application uses `Europe/Moscow` timezone by default.
*   The database is persistent using Docker volumes.