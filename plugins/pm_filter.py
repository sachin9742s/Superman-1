#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import asyncio 
import os
import imdb
import pytz, datetime
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
            google_keyword = search.replace(" ", "+")
            msg = await message.reply_text(text="""
                <b>ʜᴇʟʟᴏ {} 👋

ɪ ᴄᴏᴜʟᴅ ɴᴏᴛ ꜰɪɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀꜱᴋᴇᴅ ꜰᴏʀ 🥲

ᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴀʀᴄʜ ᴏɴ ɢᴏᴏɢʟᴇ ᴏʀ ɪᴍᴅʙ</b>
                  """.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🌟 ɪᴍᴅʙ 🌟', url='https://imdb.com'),
                        InlineKeyboardButton('⚡ ɢᴏᴏɢʟᴇ ⚡️', url=f'https://www.google.com/search?q={google_keyword}')
                    ],
                    [
                        InlineKeyboardButton("🥲 ഒന്നും മനസ്സിലാവുന്നില്ലലോ 🥲", callback_data="no_results")
                    ]
                ]
            )
        )
            await asyncio.sleep(20)
            await message.delete()
            await msg.delete()
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

            search = message.text
            ia = imdb.IMDb()
            movies = ia.search_movie(search)
            if movies:
                fileid = movies[0].get_fullsizeURL()
                await message.reply_photo(photo=fileid, 
                    caption=f"""<b>Hey 👋 ||{message.from_user.mention}|| 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                    reply_markup=InlineKeyboardMarkup(buttons))
            else:    
                await message.reply_text(f"""<b>Hey 👋 ||{message.from_user.mention}|| 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                    reply_markup=InlineKeyboardMarkup(buttons))
        btns = list(split_list(btn, 10)) 
        keyword = f"{message.chat.id}-{message.id}"
        BUTTONS[keyword] = {
            "total" : len(btns),
            "buttons" : btns
        }
        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="ᑎᗴ᙭T 🔜",callback_data=f"next_0_{keyword}")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        search = message.text
        ia = imdb.IMDb()
        movies = ia.search_movie(search)
        if movies:
            fileid = movies[0].get_fullsizeURL()
            await message.reply_photo(photo=fileid, 
                caption=f"""<b>Hey 👋 ||{message.from_user.mention}|| 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                reply_markup=InlineKeyboardMarkup(buttons))
        else:    
            await message.reply_text(f"""<b>Hey 👋 ||{message.from_user.mention}|| 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                reply_markup=InlineKeyboardMarkup(buttons))
    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 ᗷᗩᑕK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 ᗷᗩᑕK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("ᑎᗴ᙭T 🔜", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 ᗷᗩᑕK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                mention=query.from_user.mention
                m = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                time = m.hour

                if time < 12:
                    get="Good Morning"
                elif time < 15:
                    get="Good Afternoon"
                elif time < 20:
                    get="Good Evening"
                else:
                    get="Good Night"
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption, mention=query.from_user.mention)
                    except Exception as e:
                        print(e)
                        f_caption=f"""**👋 Hey {mention} 😍, **

<code>[CB].{title}</code>

**{size}

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

{get} {mention} 💐

<i>Because of copyright this file will be deleted from here within 10 minutes
So forward it to anywhere before downloading!

കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഈ ഫയൽ 10 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ്
അതുകൊണ്ട് ഇവിടെ നിന്നും മറ്റെവിടെക്കെങ്കിലും മാറ്റിയതിന് ശേഷം ഡൗൺലോഡ് ചെയ്യുക**</i>"""
                if f_caption is None:
                    f_caption = f""" **👋 Hey {mention} 😍,**

<code>[CB].{title}</code>

**{size}

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

{get} {mention} 💐

<i>Because of copyright this file will be deleted from here within 10 minutes
So forward it to anywhere before downloading!

കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഈ ഫയൽ 10 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ്
അതുകൊണ്ട് ഇവിടെ നിന്നും മറ്റെവിടെക്കെങ്കിലും മാറ്റിയതിന് ശേഷം ഡൗൺലോഡ് ചെയ്യുക</i>**"""
                buttons = [
                    [
                        InlineKeyboardButton('ᴊᴏɪɴ ɴᴏᴡ ⚫️', url='https://t.me/+yn4CU4occNU2NGNl')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=SEND_CHANNEL,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                
                
                humm = [[
                        InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"{filess.link}")
                        ],[
                        InlineKeyboardButton("⚠️ ᴄᴀɴ'ᴛ ᴀᴄᴄᴇꜱꜱ❓ ᴘʀᴇꜱꜱ ʜᴇʀᴇ ⚠️", url=f"https://t.me/+7kg9oZVwlENiMmNl")
                        ]]
                reply_markup=InlineKeyboardMarkup(humm)
                msg1 = await query.message.reply(text=f"""**<i>Hey 👋 {query.from_user.mention} 😍

📫 ʏᴏᴜʀ Fɪʟᴇ ɪꜱ Rᴇᴀᴅʏ 👇

📂 Mᴏᴠɪᴇ Nᴀᴍᴇ :<code>[CB].{title}</code>

⚙️ Mᴏᴠɪᴇ Sɪᴢᴇ : {size}</i>**

<code>𝖳𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖺𝖿𝗍𝖾𝗋 10 𝗆𝗂𝗇𝗎𝗍𝖾𝗌</code>""", reply_markup=reply_markup)
                await asyncio.sleep(600)
                await msg1.delete()
                
                return  
        


        elif query.data == "pages":
            await query.answer("No Use", show_alert=False)
        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()
        elif query.data == "no_results":
            await query.answer("സിനിമ ലഭിക്കണം എങ്കിൽ താങ്കൾ ഗൂഗിൾ നോക്കി സിനിമയുടെ correct spelling ഇവിടെ send ചെയ്യുക എങ്കിലേ താങ്കൾ ഉദ്ദേശിക്കുന്ന സിനിമ എനിക്ക് അയച്ചു തരാൻ കഴിയുകയുള്ളു 😊", show_alert=True)
                
    else:
        await query.answer("Not For You !",show_alert=True)
