#!/bin/bash
# run_universitydb_gui.sh: Skrypt uruchamiający aplikację Kivy

# Ustawienie PYTHONPATH na główny katalog projektu
export PYTHONPATH=$(pwd)

# Uruchomienie aplikacji Kivy
python -m clients.gui_kivy.main
