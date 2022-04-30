#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import os
from utils import get_filter_results, get_file_details
BUTTONS = {}
BOT = {}
SEND_CHANNEL = int(os.environ.get("SEND_CHANNEL"))
SEND_USERNAME = os.environ.get("SEND_USERNAME")
    
@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"📁 {filename}", callback_data=f"subinps#{file_id}")]
                )
        else:
            msg = await message.reply_text(text="""
                <b>Hello {} I could not find the movie you asked for...
Google, IMDB Click on any button and find the <u>CORRECT MOVIE NAME</u> and enter it here but the movie will be available...
If you do not receive the movie even after entering the correct name...  <code>@admin type movie name</code> Inform the admin in this format.. We will upload within 24 hours </b>
                  """.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🌟 ɪᴍᴅʙ 🌟', url='https://imdb.com'),
                        InlineKeyboardButton('⚡ ɢᴏᴏɢʟᴇ ⚡️', url='https://www.google.com')
                    ],
                    [
                        InlineKeyboardButton("🥲 ഒന്നും മനസ്സിലാവുന്നില്ലലോ 🥲", callback_data="no_results")
                    ]
