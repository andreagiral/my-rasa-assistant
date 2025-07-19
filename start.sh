#!/bin/bash
echo "✅ Starting Rasa Action Server..."
echo "Rasa SDK version: $(pip show rasa-sdk | grep Version)"
echo "Python version: $(python --version)"
rasa run actions --port 8000 --debug


