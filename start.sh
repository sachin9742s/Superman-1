echo "Cloning Repository"
git clone https://<pat>@github.com/JoelBobanOffline/Lauren_Remastered.git
cd Lauren_Remastered
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
