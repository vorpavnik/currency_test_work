FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip==23.3.1 setuptools wheel pytest pytest-django

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it

COPY . /app

CMD ["bash", "-c", "wait-for-it db:5432 --timeout=60 && sleep 10 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]