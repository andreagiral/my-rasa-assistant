#!/bin/bash
echo "✅ Starting Rasa Web Server..."
echo "Rasa version: $(rasa --version)"

rasa run --enable-api \
         --cors "*" \
         --port 5005 \
         --model models/AI2.3.tar.gz \
         --endpoints endpoints.yml \
         --credentials credentials.yml \
         --debug \

echo "❌ Rasa Web Server exited unexpectedly."
