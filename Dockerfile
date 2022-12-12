# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /dockerized_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /dockerized_app/

ENV FLASK_APP=/dockerized_app/app/main.py

ENTRYPOINT ["python3"]
CMD ["app/main.py"]

