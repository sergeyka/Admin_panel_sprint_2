FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements /requirements

# install psql
RUN apt-get update && apt-get -y install postgresql-client

RUN pip3 install -r /requirements/production.txt
COPY . /code/
EXPOSE 80

# git doesn't track permissions, so make the file executable inside the container.
RUN ["chmod", "+x", "./entrypoint.sh"]
RUN ["chmod", "+x", "./wait-for-postgres.sh"]

ENTRYPOINT ["./entrypoint.sh"]

