# Use official Python slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for wkhtmltopdf and others
RUN apt-get update && apt-get install -y \
    wget \
    fontconfig \
    libxrender1 \
    libjpeg62-turbo \
    libpng16-16 \
    libssl-dev \
    libx11-6 \
    libxcb1 \
    libxext6 \
    xfonts-base \
    xfonts-75dpi \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Download and install wkhtmltopdf (version 0.12.6 for Debian Buster)
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || true \
    && apt-get update && apt-get install -f -y \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port (Streamlit default port)
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
