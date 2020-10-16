FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /webapp
RUN mkdir /bot
RUN apt update

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./webapp /webapp/
COPY ./bot /bot/
CMD gunicorn --bind=0.0.0.0:8080 --name=webapp webapp.wsgi:application --reload -w 2
