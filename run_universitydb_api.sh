#!/bin/bash

# Ustawienie PYTHONPATH na główny katalog projektu
export PYTHONPATH=$(pwd)

# Uruchomienie aplikacji FastAPI przy użyciu uvicorn
uvicorn clients.web.main:app --reload --host 0.0.0.0 --port 8000
