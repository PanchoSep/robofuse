FROM python:3.11-slim

ARG PUID=1000
ARG PGID=1000

LABEL maintainer="robofuse Team"
LABEL description="robofuse - A service that interacts with Real-Debrid API to generate .strm files"

# Create non-root user with custom UID/GID
RUN addgroup --gid $PGID appgroup && \
    adduser --disabled-password --gecos "" --uid $PUID --gid $PGID appuser

# Set working directory
WORKDIR /app

# Install system dependencies including git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir git+https://github.com/dreulavelle/PTT.git

# Copy the application code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create directories
RUN mkdir -p /app/Library /app/cache

# Cambia permisos y usa el nuevo usuario
RUN chown -R appuser:appgroup /app
USER appuser

# Use non-root user
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set default command
CMD ["python", "-m", "robofuse", "watch"]

# Expose documentation (not required for functionality)
EXPOSE 8000 
