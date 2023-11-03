# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /myproject

# Copy the requirements file into the container
COPY requirements.txt /myproject/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install eventlet for gunicorn
RUN pip install eventlet==0.30.2

# Copy the rest of the Django app code to the container
COPY . /myproject/

# Expose the port on which the Django app will run
EXPOSE 8000

# Define the command to run the Django app with gunicorn using eventlet
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "Chat.wsgi:application"]
