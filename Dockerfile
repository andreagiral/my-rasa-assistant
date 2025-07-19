FROM rasa/rasa-sdk:3.1.0

WORKDIR /app

COPY . /app

# Install Python packages globally (inside container)
USER root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x /app/start.sh
    
EXPOSE 8000

CMD ["/app/start.sh"]
