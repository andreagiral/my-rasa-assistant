FROM rasa/rasa:3.5.10

WORKDIR /app
COPY . /app

USER root

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh

EXPOSE 5005
CMD ["./start.sh"]
