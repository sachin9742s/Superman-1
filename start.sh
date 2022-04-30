echo "Cloning Repository"
git clone https://<pat>@github.com/JoelBobanOffline/Lauren_Remastered.git /Lauren
fi
cd /Lauren
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
