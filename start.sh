#!/bin/bash
echo "✅ Starting Rasa Action Server..."
echo "Rasa SDK version:"
pip show rasa-sdk

echo "Python version:"
python --version

echo "⚙️ Running Rasa SDK action server..."
python -m rasa_sdk --port 8000 --debug

echo "❌ Action Server exited unexpectedly."
