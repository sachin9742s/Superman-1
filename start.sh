echo "Cloning Repository"
git clone https://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@github.com/JoelBobanOffline/Lauren_Remastered.git /Lauren
fi
cd /Lauren
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
