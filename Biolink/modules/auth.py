# Copyright ©️ by Akash Dakshwanshi 
from pyrogram import filters
from pyrogram.types import Message
from Biolink import Biolink as app
from Biolink.helper.auth import add_auth, remove_auth, get_auth_users
from Biolink.helper.admin import is_admins

def format_user(user):
    username = f"@{user.username}" if user.username else "No Username"
    mention = user.mention(style="markdown")
    return f"**Name:** {mention}\n**User ID:** `{user.id}`\n**Username:** `{username}`"

async def get_target_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(message.command) > 1:
        username = message.text.split(None, 1)[1].strip()
        try:
            user = await app.get_users(username)
            return user
        except:
            return None
    return None

@app.on_message(filters.command("auth", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group)
async def add_auth_command(client, message: Message):
    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply("❌ Only group owner or admins can use this command!")

    user = await get_target_user(message)
    if not user:
        return await message.reply("Reply to a user or give a valid username/user ID!")

    await add_auth(message.chat.id, user.id)
    await message.reply(f"✅ User has been **authorized**.\n\n{format_user(user)}")

@app.on_message(filters.command("rmauth", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group)
async def remove_auth_command(client, message: Message):
    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply("❌ Only group owner or admins can use this command!")

    user = await get_target_user(message)
    if not user:
        return await message.reply("Reply to a user or give a valid username/user ID!")

    await remove_auth(message.chat.id, user.id)
    await message.reply(f"❌ User has been **unauthorized**.\n\n{format_user(user)}")

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("authlist", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group)
async def authlist_handler(client, message: Message):
    # Check if user is admin
    if not await is_admins(message.chat.id, message.from_user.id):
        return await message.reply("❌ Only group owner or admins can use this command!")

    chat_id = message.chat.id
    data = await get_auth_users(chat_id)
    users = data.get("auth_users", [])

    if not users:
        return await message.reply("⚠️ No users have been authorized in this group.")

    text = "**Authorized users in this group:**\n\n"
    for i, user_id in enumerate(users, start=1):
        try:
            user = await app.get_users(user_id)
            name = user.mention(style="markdown")
        except:
            name = f"`{user_id}` (Unable to fetch)"
        text += f"{i}. {name}\n"

    # Send message with Close button
    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗑 Close", callback_data="close")]]
        )
    )
