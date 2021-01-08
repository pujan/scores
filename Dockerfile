FROM python:3
LABEL pl.bookmarks.vendor="Łukasz A. Pelc"
LABEL version="1.0"
LABEL description="API - scores sport teams"
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -U -r requirements.txt
COPY . /code/
