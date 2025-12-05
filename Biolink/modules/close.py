#𝐀𝐚𝐬𝐡𝐢𝐤 𝐓ᴇᴀᴍ
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from Biolink import Biolink as app

@app.on_callback_query(filters.regex("close"))
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
        closed = await query.message.reply_text(
            f"✅ Closed by : {query.from_user.mention}"
        )
        await asyncio.sleep(2)
        await closed.delete()
    except:
        pass
