# Use an official Python image as a base
FROM python:3.9-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY migrations ./migrations

EXPOSE 8000

CMD ["sh", "-c", "pytest && alembic upgrade head  && uvicorn main:app --host 0.0.0.0 --port 8000"]