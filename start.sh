#!/bin/bash
echo "✅ Starting Rasa Action Server..."
echo "Rasa SDK version:"
pip show rasa-sdk

echo "Python version:"
python --version

echo "⚙️ Running Rasa Action Server on port 8000..."
rasa run actions --port 8000 --debug

echo "❌ Action Server exited unexpectedly."
