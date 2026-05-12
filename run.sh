#!/bin/bash
echo "Starting Swimming Lesson Dashboard..."
echo ""
echo "Once started, your dashboard will open automatically in your browser."
echo "To stop the server, press Ctrl+C."
echo ""
pip install -r requirements.txt --quiet
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
