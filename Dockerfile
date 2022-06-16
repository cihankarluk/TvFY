FROM python:3.9.10

# set env
ENV DJANGO_SETTINGS_MODULE itests.settings

# copy source code
COPY . /app
WORKDIR /app

RUN pip install .
