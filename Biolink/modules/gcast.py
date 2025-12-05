import asyncio
from pyrogram.errors import PeerIdInvalid, UserIsBlocked, InputUserDeactivated, FloodWait
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from config import OWNER_ID
from Biolink.helper.database import get_users, get_chats
from Biolink import Biolink as app

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Please reply to a message to broadcast.")

    sent = 0
    failed = 0

    # Get user and chat list
    users_data = await get_users()
    chats_data = await get_chats()

    targets = set(users_data["users"] + chats_data["chats"])

    status = await message.reply(
        f"▣ Starting broadcast...\n\n"
        f"Total targets: {len(targets)}"
    )

    for uid in targets:
        try:
            await client.copy_message(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.id
            )
            sent += 1
            await asyncio.sleep(0.05)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except (PeerIdInvalid, UserIsBlocked, InputUserDeactivated):
            failed += 1
        except Exception:
            failed += 1

    await status.edit(
        f"✅ Broadcast completed!\n\n"
        f"Total Targets: {len(targets)}\n"
        f"✅ Success: {sent}\n"
        f"⛔ Failed: {failed}"
    )
