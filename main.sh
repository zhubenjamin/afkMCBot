
source .venv/bin/activate

while true
    do
        python3 afkBot/bot.py
        echo "Restarting in 5 seconds..."
        sleep 5
    done