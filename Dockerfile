# pull official base image
#FROM python:3.8-slim-buster
FROM informaticsmatters/rdkit-python3-debian

USER root

RUN useradd standarduser

# set work directory
WORKDIR /usr/src/lab_man1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/bin/"

# install psycopg2 dependencies
RUN apt-get update -y
RUN apt-get install -y libpq-dev gcc python3-dev musl-dev netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

USER standarduser

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/lab_man1/entrypoint.sh"]
