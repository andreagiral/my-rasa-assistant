FROM rasa/rasa:3.1.0

WORKDIR /app

COPY . /app

USER root

RUN chmod +x /app/start.sh

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--model", "models/AI2.3.tar.gz", "--endpoints", "endpoints.yml", "--credentials", "credentials.yml", "--debug"]
