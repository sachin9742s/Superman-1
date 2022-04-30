#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import os
from utils import get_filter_results, get_file_details
BUTTONS = {}
BOT = {}
SEND_CHANNEL = os.environ.get(["SEND_CHANNEL"])
SEND_USERNAME = os.environ.get(["SEND_USERNAME"])

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
                    [InlineKeyboardButton(text=f"📁 {filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            msg = await message.reply_text(text="""
                <b>Hello {} I could not find the movie you asked for...
Google, IMDB Click on any button and find the <u>CORRECT MOVIE NAME</u> and enter it here but the movie will be available...
If you do not receive the movie even after entering the correct name...  <code>@admin type movie name</code> Inform the admin in this format.. We will upload within 24 hours </b>
                  """.format(message.from_user.mention),
                 parse_mode="html",
                 reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('🌟 ɪᴍᴅʙ 🌟', url='https://imdb.com'),
                        InlineKeyboardButton('⚡ ɢᴏᴏɢʟᴇ ⚡️', url='https://www.google.com')
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
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")]
            await message.reply_text(f"""<b>Hey 👋 {message.from_user.mention} 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                parse_mode="html", 
                reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        await message.reply_text(f"""<b>Hey 👋 {message.from_user.mention} 😍

📁 Found ✨  Files For Your Query : {search} 👇</b>""", 
                parse_mode="html", 
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
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
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
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
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
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
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
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
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
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Join Here 👻', url='https://t.me/joel_noob')
                    ]
                    ]
                
                await query.answer()
                filess = await client.send_cached_media(
                    chat_id=SEND_CHANNEL,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                message = query.message.reply_to_message
                humm = [[
                        InlineKeyboardButton("📥 Download Link 📥", url=f"{filess.link}")
                        ],[
                        InlineKeyboardButton("⚠️ Can't Access❓ Click Here ⚠️", url=f"https://t.me/{SEND_USERNAME}")
                        ]]
                reply_markup=InlineKeyboardMarkup(humm)
                await message.reply_text(text=f"""Hey 👋 {query.from_user.mention} 😍

📫 Yᴏʀ Fɪʟᴇ ɪꜱ Rᴇᴀᴅʏ 👇

📂 Mᴏᴠɪᴇ Nᴀᴍᴇ : {title}

⚙️ Mᴏᴠɪᴇ Sɪᴢᴇ : {size}""", reply_markup=reply_markup)
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
