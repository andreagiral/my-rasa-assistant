FROM rasa/rasa-sdk:3.1.0

WORKDIR /app

COPY . /app

# Install Python packages globally (inside container)
USER root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Give execute permission to your script
RUN chmod +x start.sh

CMD ["./start.sh"]
