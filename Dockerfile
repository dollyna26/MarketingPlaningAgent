# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Avoid unnecessary logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for some Python libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt

# Copy all project files
COPY . .

# Expose port (for web apps)
EXPOSE 8000

# Default command (change if needed)
CMD ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]