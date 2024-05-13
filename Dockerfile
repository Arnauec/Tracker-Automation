# Use selenium/standalone-chrome as a parent image
FROM selenium/standalone-chrome

# Install Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt