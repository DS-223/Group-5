FROM python:3.10-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /ds

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all other project files
COPY . .

# Expose your service port
EXPOSE 3000

# Default command
CMD ["python", "ds_main.py"]