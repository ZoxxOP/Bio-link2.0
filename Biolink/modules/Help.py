from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Biolink import Biolink as app

@app.on_callback_query(filters.regex("^show_help$"))
async def show_help(_, query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Admin Commands", callback_data="help_admin")],
            [InlineKeyboardButton("Other Commands", callback_data="help_misc")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
    )
    await query.message.edit_text(
        "**Help Menu**\nSelect a category below:",
        reply_markup=keyboard
    )

# Admin Commands
@app.on_callback_query(filters.regex("^help_admin$"))
async def help_admin(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Admin Commands:**
• /auth - bio user
• /rmauth - bio user
• /biolink on
• /biolink off""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Back", callback_data="show_help")]]
        )
    )


# Misc Commands
@app.on_callback_query(filters.regex("^help_misc$"))
async def help_misc(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Other Commands:**
• /start - Start the bot
• /stats - Bot statistics
• /addsudo - Add sudo user
• /delsudo - Remove sudo
• /broadcast - broadcast""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Back", callback_data="show_help")]]
        )
    )
