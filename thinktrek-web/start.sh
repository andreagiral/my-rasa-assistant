#!/bin/bash
echo "✅ Starting Rasa Web Server..."
rasa run \
  --enable-api \
  --cors "*" \
  --debug \
  --endpoints endpoints.yml \
  --port 5005
