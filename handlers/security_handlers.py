from config import SPECIAL_USERS
from telegram import Update, InputMediaPhoto
from telegram.ext import (
    ContextTypes,
    ApplicationHandlerStop,
)


async def security_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.name in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text(
            "Hey! You are not allowed to use me! 🚨🚓"
        )
        raise ApplicationHandlerStop


# Further Ideas:
# Adding/Removing Users to the Bot dynamically
