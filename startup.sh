#!/bin/bash
# Start FastAPI Backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 &
 
# Start Nginx to Serve React Frontend
nginx -g "daemon off;"