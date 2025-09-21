#!/bin/bash
cd /home/chirimoya/projects/taskTracker/backend
exec /home/chirimoya/projects/taskTracker/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload