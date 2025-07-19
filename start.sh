#!/bin/bash

# Train the model
rasa train

# Start both action server and rasa server in background
rasa run actions --port 5055 &
rasa run --enable-api --cors "*" --debug

chmod +x start.sh
