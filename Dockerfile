# Use the full Rasa image that includes training tools
FROM rasa/rasa:3.1.0-full

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your repo into the container
COPY . /app

# Train your assistant when the container is built
RUN rasa train

# Run the Rasa server with API access and debugging enabled
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
