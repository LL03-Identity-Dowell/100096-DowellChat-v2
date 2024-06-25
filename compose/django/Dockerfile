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

# Copy the entrypoint script into the container
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose the port on which the Django app will run
EXPOSE 8001

# Set the entrypoint to the script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
