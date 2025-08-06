FROM rasa/rasa:3.6.10

WORKDIR /app

COPY . /app

USER root

RUN chmod +x /app/start.sh

EXPOSE 5005

CMD ["./start.sh"]
