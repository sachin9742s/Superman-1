echo "Cloning Repo"
  git clone ttps://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@github.com/JoYaL-TG/Superman.git
fi
cd /Superman
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
