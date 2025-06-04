# Use official Python slim image as base
FROM python:3.10-slim

# Install wkhtmltopdf dependencies and wkhtmltopdf itself
RUN apt-get update && apt-get install -y \
    wget \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    libxrender1 \
    libssl-dev \
    libx11-6 \
    libjpeg62-turbo \
    libglib2.0-0 \
    libxext6 \
    libxtst6 \
    libpng-dev \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Download wkhtmltopdf binary (version 0.12.6) and install
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose the port that Streamlit uses
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
