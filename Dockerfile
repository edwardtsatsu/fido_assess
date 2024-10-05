# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /src

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy Alembic migrations
COPY migrations ./migrations

# Expose the port FastAPI runs on
EXPOSE 8000

# Run Alembic migrations and then start the FastAPI application
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
