FROM python:3.9.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 2

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000