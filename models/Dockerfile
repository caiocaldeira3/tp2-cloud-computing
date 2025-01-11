# Base image
FROM python:3.12.8-slim-bullseye

# Set working directory
WORKDIR /models

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rule generation script
COPY recommend_model.py .
COPY service.env .

# Set the default command to generate rules
CMD ["python", "recommend_model.py"]
