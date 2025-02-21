#!/bin/bash

# Start the uvicorn processes
uvicorn bands.main:app --port 8000 & 
BANDS_PID=$!
uvicorn reviews.main:app --port 8080 & 
REVIEWS_PID=$!

# Wait for a few seconds to ensure the servers are up
sleep 3

# Execute the run.py Python module
python3 run.py

# Wait for a few seconds to ensure the SigNoz receives signals
sleep 1

# Kill the uvicorn processes
kill $BANDS_PID
kill $REVIEWS_PID