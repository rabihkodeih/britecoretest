# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.6

# install postgres client
RUN apt-get update -y && apt-get install -y postgresql-9.6 

# disable buffering for terminal output
ENV PYTHONUNBUFFERED 1

# create root directory for project in the container
RUN mkdir /britecore

# Set the working directory to /mango
WORKDIR /britecore

# Copy the current directory contents into the container at /mango
ADD . /britecore

# install dependencies
RUN pip3 install -r requirements.txt

# setup the container entrypoint
ENTRYPOINT ["gunicorn", "britecore.wsgi", "-b", "0.0.0.0:8000"]
