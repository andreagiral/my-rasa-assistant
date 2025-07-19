FROM rasa/rasa:3.1.0-full

WORKDIR /app

COPY . /app

# Install custom dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 5005
EXPOSE 5055

# Start script
CMD ["./start.sh"]
