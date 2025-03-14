# Pull base image
FROM python:3.10.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code/backend

# Copy requirements file & install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install uv
RUN uv pip install -r requirements.txt --system

RUN apt-get update && apt-get install -y libcairo2-dev libjpeg-dev libpng-dev

# Copy project
COPY . /code/backend/


USER root
