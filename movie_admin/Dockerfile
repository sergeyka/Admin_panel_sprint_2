FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements /requirements
RUN pip3 install -r /requirements/production.txt
COPY . /code/
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]

