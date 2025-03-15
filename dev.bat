@echo off
poetry run uvicorn crafty.main:app --host 127.0.0.1 --port 4000 --reload
