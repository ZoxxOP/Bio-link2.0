# Copyright ©️ by Akash Dakshwanshi 
import time
import psutil
import platform
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Biolink import Biolink as app
from config import OWNER_ID

# Import your user/chat count functions
from Biolink.helper.usersdb import get_users
from Biolink.helper.chatsdb import get_chats

START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        if seconds == 0:
            break
        seconds, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        time_list.append(f"{int(result)}{time_suffix_list[count - 1]}")
    return ":".join(time_list[::-1])

@app.on_message(filters.command("status") & filters.user(OWNER_ID))
async def bot_status(_, message: Message):
    current_time = time.time()
    uptime = get_readable_time(int(current_time - START_TIME))
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    platform_info = platform.system() + " " + platform.release()

    users_count = await get_users()
    chats_count = await get_chats()

    await message.reply_text(
        f"**✨ ʙᴏᴛ sᴛᴀᴛᴜs ✨**\n\n"
        f"**⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯**\n"
        f"**ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"**ᴄᴘᴜ ᴜsᴀɢᴇ:** `{cpu}%`\n"
        f"**ʀᴀᴍ ᴜsᴀɢᴇ:** `{ram}%`\n"
        f"**ᴘʟᴀᴛғᴏʀᴍ:** `{platform_info}`\n"
        f"**ᴜsᴇʀs:** `{users_count}`\n"
        f"**ᴄʜᴀᴛs:** `{chats_count}`\n"
        f"**⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close_status")]
        ])
    )

@app.on_callback_query(filters.regex("close_status"))
async def close_status_callback(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
    await query.answer("Closed", show_alert=False)
