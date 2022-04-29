echo "Cloning Repository"
git clone https://github.com/EvamariaTG/EvaMaria.git /Lauren
fi
cd /Lauren
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
