# Base image
FROM python:3.12.8-slim-bullseye

# Set working directory
WORKDIR /server

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV VERSION=0.92
ENV DATE=10-01-2025
ENV MODEL_PATH="/project2-pv2/rules.pkl"

# Copy the Flask app
COPY app.py .
COPY models.py .
COPY service.env .
COPY static static
COPY templates templates

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=5000

# Expose port 5000
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]
