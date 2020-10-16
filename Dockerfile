FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /webapp
RUN mkdir /bot
#WORKDIR /webapp
COPY requirements.txt .
COPY entrypoint.sh /webapp
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./webapp /webapp/
COPY ./bot /bot/
WORKDIR /webapp

RUN pwd
RUN ls -la
#CMD python bot.py
#RUN python bot.py
# apt install
# pip install --upgrade pip
# pip install -r requirements.txt
# COPY webapp
# WORKDIR /webapp/
# python bot.py