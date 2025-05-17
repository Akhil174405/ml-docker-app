# Use a lightweight Python image
FROM python:3.13.2-slim

# Set working directory inside container
WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port 5000 (or whichever port you want FastAPI to run on)
EXPOSE 5000

# Run the app using uvicorn (production-ready ASGI server)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
