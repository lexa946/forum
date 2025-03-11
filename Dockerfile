FROM python:3.12-slim

LABEL authors="pozhar"

COPY app ./app
COPY requirements.txt requirements.txt
COPY *.py ./
COPY *.ini ./
COPY .env /.env

RUN pip install -r requirements.txt

RUN alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]