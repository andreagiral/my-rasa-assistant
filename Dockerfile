FROM rasa/rasa-sdk:3.1.0

WORKDIR /app

COPY actions/actions.py .
COPY config.yml .
COPY domain.yml .
COPY endpoints.yml .
COPY data/nlu.yml .
COPY data/rules.yml .
COPY data/stories.yml .
COPY credentials.yml .

# ✅ Install Python packages without permission issues
RUN pip install --user --no-cache-dir openai boto3 python-dotenv beautifulsoup4

# Optional: remove rasa train from here if your Render service only runs actions
RUN rasa train  

CMD ["rasa", "run", "--enable-api", "--debug", "--cors", "*"]
