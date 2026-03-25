#!/bin/bash

while true
    do
        .venv/bin/python3 bot.py
        echo "Restarting in 5 seconds..."
        sleep 5
    done