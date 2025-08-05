#!/bin/bash
echo "✅ Starting Rasa Web Server..."
echo "Rasa version: $(rasa --version)"

rasa run --enable-api \
         --cors "*" \
         --port 5005 \
         --model ../models/latest.tar.gz \
         --endpoints thinktrek-web/endpoints_render.yml \
         --credentials ../credentials.yml \
         --debug \

echo "❌ Rasa Web Server exited unexpectedly."
