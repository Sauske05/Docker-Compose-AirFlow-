# Use Python as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files
COPY model.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "model.py"]