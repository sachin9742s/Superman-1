import heroku3
import os
from pyrogram import Client, filters
from info import ADMINS

API_KEY = os.environ.get("API_KEY")
APP_NAME = os.environ.get("APP_NAME")

async def app_restart():
    beroku = heroku3.from_key(API_KEY)
    app = beroku.apps()[APP_NAME]
    if API_KEY:
        app.restart()
    else:
        return


@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restarts(client, message):
    if API_KEY:
        await message.reply_text("Trying to restart")
        await app_restart()
    else:
        await message.reply_text("Api key not found!")
