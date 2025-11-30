# Base Image

FROM python:3.13-slim

# working directory

WORKDIR /app

# Copy Requirements

COPY requirements.txt .

# Install Requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy Files 

COPY . .

# Expose Port

EXPOSE 8000

# Run Command

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


