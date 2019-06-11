FROM python:3.5-alpine

RUN adduser -D chatbot

WORKDIR /home/chatbot

COPY setup.py setup.py
COPY alice alice
COPY migrations migrations
COPY rasa rasa
COPY config.py boot.sh ./


RUN python -m venv venv
RUN venv/bin/python setup.py install

RUN venv/bin/pip install gunicorn

RUN chmod +x boot.sh

ENV FLASK_APP alice

RUN chown -R chatbot:chatbot ./
USER chatbot

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
