FROM rasa/rasa:3.1.0-full

WORKDIR /app

COPY actions.py .
COPY config.yml .
COPY domain.yml .
COPY endpoints.yml .
COPY nlu.yml .
COPY rules.yml .
COPY stories.yml .
COPY credentials.yml .

RUN pip install --no-cache-dir openai boto3 python-dotenv beautifulsoup4

RUN rasa train

CMD ["rasa", "run", "--enable-api", "--debug", "--cors", "*"]
