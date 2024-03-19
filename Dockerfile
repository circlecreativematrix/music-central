# Use the official Python 3.10.2 image as the base image
FROM python:3.10.2

# Set the working directory in the container
WORKDIR /app

# Copy all python files in the root directory to the container
COPY ./*.py /app/

# Copy the public folder to the container
COPY ./public /app/public
COPY ./config /app/config
# Copy the requirements.txt file to the container
COPY ./requirements.txt /app/

# Install the required Python packages
RUN pip install -r requirements.txt

# Expose port 8888 for the server
EXPOSE 8888

# Set the entrypoint command to run the Server.py file
CMD ["python", "Server.py"]
