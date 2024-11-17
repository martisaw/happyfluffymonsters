from config import MONSTER_MONDAY_CHAT_ID
from handlers.job_queue_static import monster_monday_reminder_greetings
import random
from telegram.ext import ContextTypes


async def monster_monday_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=MONSTER_MONDAY_CHAT_ID,
        text=random.choice(monster_monday_reminder_greetings),
    )
