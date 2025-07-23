#!/bin/bash
echo "✅ Starting Rasa Web Server..."
echo "Rasa version: $(rasa --version)"

rasa run --enable-api \
         --cors "*" \
         --port 5005 \
         --endpoints endpoints_render.yml \
         --debug \
         --model models \

echo "❌ Rasa Web Server exited unexpectedly."
