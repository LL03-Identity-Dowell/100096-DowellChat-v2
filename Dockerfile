FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Remember to clean your package manager cache to reduce your custom image size...
RUN apt-get clean all \
   && rm -rvf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the Django app code to the container
COPY . /usr/src/app

# RUN python manage.py makemigrations
# RUN python manage.py migrate
# Install dependencie

# Expose the port on which the Django app will run
EXPOSE 8001

# Update the CMD to run uWSGI for your application
# CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "Chat.wsgi:application", "--timeout", "1060", "-b", ":8000"]
