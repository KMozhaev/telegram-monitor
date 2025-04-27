FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create data directory for SQLite DB and session file
RUN mkdir -p /app/data

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
