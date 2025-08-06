FROM rasa/rasa:3.1.0

WORKDIR /app

COPY . /app

USER root

RUN chmod +x /app/start.sh

EXPOSE 5005

CMD ["bash", "./start.sh"]
