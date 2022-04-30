  GNU nano 5.4                  pm_filter.py                           
#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_G>
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,>
from pyrogram import Client, filters
import re
import os
from utils import get_filter_results, get_file_details
BUTTONS = {}
BOT = {}
SEND_CHANNEL = int(os.environ.get("SEND_CHANNEL"))
SEND_USERNAME = os.environ.get("SEND_USERNAME")
    
@Client.on_message(filters.text & filters.group & filters.incoming & f>
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", mess>
        return
  GNU nano 5.4                  pm_filter.py                           
#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_G>
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,>
from pyrogram import Client, filters
import re
import os
from utils import get_filter_results, get_file_details
BUTTONS = {}
BOT = {}
SEND_CHANNEL = int(os.environ.get("SEND_CHANNEL"))
SEND_USERNAME = os.environ.get("SEND_USERNAME")
    
@Client.on_message(filters.text & filters.group & filters.incoming & f>
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", mess>
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

^G Help       ^O Write Out  ^W Where Is   ^K Cut        ^T Execute
^X Exit       ^R Read File  ^\ Replace    ^U Paste      ^J Justify
