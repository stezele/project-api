# Use an official lightweight Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies for Microsoft ODBC Driver 18
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/$(lsb_release -rs)/prod $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
