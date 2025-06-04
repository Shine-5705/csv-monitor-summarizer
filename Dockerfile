FROM python:3.11-slim

# Set work directory
WORKDIR /app

# System dependencies for wkhtmltopdf
RUN apt-get update && \
    apt-get install -y \
    wkhtmltopdf \
    build-essential \
    libxrender1 \
    libfontconfig1 \
    libxext6 \
    libjpeg-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
