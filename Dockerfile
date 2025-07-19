FROM rasa/rasa-sdk:3.1.0

#FROM rasa/rasa:3.1.0-full

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Give execute permission to start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]
