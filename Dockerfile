FROM python:3.11-slim

LABEL authors="pozhar"

COPY . .

RUN pip install -r requirements.txt && alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]