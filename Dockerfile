FROM python:3.13-alpine3.20

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
