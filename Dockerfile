FROM python:3.9.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 2

RUN mkdir /home/app
WORKDIR /home/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "sh" ,"./entrypoint.sh" ]