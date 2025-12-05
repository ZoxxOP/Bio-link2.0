import re
import asyncio
from pyrogram import filters, enums, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Biolink import Biolink as app
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, OTHER_LOGS, BOT_USERNAME
from Biolink.helper.auth import get_auth_users


# ----------------- MongoDB -----------------
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["BioFilterBot"]
bio_filter = db["bio_filter"]


# ----------------- Regex -----------------
URL_PATTERN = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)
USERNAME_PATTERN = re.compile(r"@[\w_]+", re.IGNORECASE)


# ----------------- Filter Status -----------------
async def is_enabled(chat_id: int) -> bool:
    data = await bio_filter.find_one({"chat_id": chat_id})
    if not data:
        return False
    return data.get("enabled", False)


async def set_enabled(chat_id: int, status: bool):
    await bio_filter.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True,
    )


# ----------------- Admin Check -----------------
async def is_admins(client, chat_id, user_id):
    async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False


# ----------------- Enable / Disable Commands -----------------
@app.on_message(filters.command("biolink") & filters.group)
async def bl_cmd(client, message):
    if not await is_admins(client, message.chat.id, message.from_user.id):
        return await message.reply_text("Only admins can use this command.")

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n`/biolink on`\n`/biolink off`"
        )

    state = message.command[1].lower()

    if state == "on":
        await set_enabled(message.chat.id, True)
        return await message.reply_text("✅ Bio Link Filter **Enabled**.")
    elif state == "off":
        await set_enabled(message.chat.id, False)
        return await message.reply_text("❌ Bio Link Filter **Disabled**.")
    else:
        return await message.reply_text("Use: `/biolink on` or `/biolink off`")


# ----------------- Main Bio Filter -----------------
@app.on_message(filters.group & filters.text)
async def bio_filter_handler(client, message):

    chat_id = message.chat.id
    user = message.from_user

    if not user:
        return

    # Filter disabled
    if not await is_enabled(chat_id):
        return

    # Admin ignore
    if await is_admins(client, chat_id, user.id):
        return

    # Auth ignore
    auth_data = await get_auth_users(chat_id)
    if user.id in auth_data.get("auth_users", []):
        return

    # Get bio
    try:
        user_info = await client.get_chat(user.id)
        bio = getattr(user_info, "bio", "") or ""
    except:
        bio = ""

    # No bio
    if not bio:
        return

    # Check if bio contains link OR username tag
    if not (re.search(URL_PATTERN, bio) or re.search(USERNAME_PATTERN, bio)):
        return

    # ----------------- Delete message -----------------
    try:
        await message.delete()
    except:
        pass

    mention = f"[{user.first_name}](tg://user?id={user.id})"
    username = f"@{user.username}" if user.username else "None"

    # ----------------- Warn User -----------------
    try:
        warn = await message.reply_text(
            f"⚠️ {mention}, **bio me link/username allowed nahi hai!**",
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close")]]
            ),
        )
        await asyncio.sleep(10)
        await warn.delete()
    except:
        pass

    # ----------------- Send Log -----------------
    log_text = f"""
**🚨 Bio Filter Alert**
**User:** {mention}
**Username:** {username}
**User ID:** `{user.id}`
**Group:** `{message.chat.title}`
**Chat ID:** `{chat_id}`
**Bio:** `{bio}`
"""

    try:
        await client.send_message(
            OTHER_LOGS,
            log_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Add Bot", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
            ),
        )
    except:
        pass
