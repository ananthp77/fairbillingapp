
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install bash
RUN apt-get update && apt-get install -y bash

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
#COPY . .
COPY . /app/

#ADD fairbilling.py ./app
# Specify the default command to run your application
CMD ["python", "fairbilling.py"]
