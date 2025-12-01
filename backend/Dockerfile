# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 7860 for Hugging Face Spaces (use 8000 for local development)
EXPOSE 7860

# Define environment variable
ENV MODULE_NAME="src.main"
ENV VARIABLE_NAME="app"
ENV PORT=7860

# Run uvicorn when the container launches
# Hugging Face Spaces uses port 7860 by default
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
