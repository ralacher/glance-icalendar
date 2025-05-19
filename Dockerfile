# Use official Python image as base
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY main.py ./
COPY pyproject.toml ./
COPY uv.lock ./

# Install pip and uv (for dependency management)
RUN pip install --no-cache-dir uvicorn fastapi httpx

# Expose the port
EXPOSE 8009

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]
