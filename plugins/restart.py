import heroku3
import os

API_KEY = os.environ.get("API_KEY", "")

async def restart():
    beroku = heroku3.from_key(API_KEY)
    app = beroku.apps()
    if API_KEY:
        app.restart()
    else:
        return
