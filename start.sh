#!/bin/bash
echo "✅ Starting Rasa Action Server..."
echo "Rasa SDK version: $(pip show rasa-sdk | grep Version)"
echo "Python version: $(python --version)"

echo "⚙️ Running Rasa SDK action server..."
rasa run actions --actions actions --port 8000 --debug
#python -m rasa_sdk --port 8000 --debug
echo "❌ Action Server exited unexpectedly."


