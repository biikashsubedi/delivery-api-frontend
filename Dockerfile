# Base Image
FROM python:3.11-slim

# Working Directory
WORKDIR /app

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Files
COPY main.py .
COPY delivery_model.joblib .

# Set Default Port for Cloud Run
ENV PORT=8080

# Run Server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]