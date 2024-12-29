#!/bin/bash

# Ustawienie PYTHONPATH na główny katalog projektu
export PYTHONPATH=$(pwd)

# Uruchomienie aplikacji konsolowej
python -m clients.cli.main
