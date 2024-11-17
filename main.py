from datetime import time
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    TypeHandler,
)
from config import BOT_TOKEN

from handlers.security_handlers import security_callback_handler
from handlers.job_queue_handlers import monster_monday_reminder
from handlers.conversation_handlers import (
    PROMPT,
    start_handler,
    cancel_handler,
    prompt_handler,
    rerun_handler,
    monstergpt_handler,
)


logger = logging.getLogger(__name__)

# ToDo build async also within services and facades
# See e.g. https://stackoverflow.com/questions/76625766/python-telegram-bot-v20-run-asynchronously


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    security_handler = TypeHandler(Update, security_callback_handler)
    application.add_handler(
        security_handler, -1
    )  # Default is 0, so we are giving it a number below 0

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_handler),
            CommandHandler("monstergpt", monstergpt_handler),
            CommandHandler("rerun", rerun_handler),
        ],
        states={
            PROMPT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, prompt_handler),
                CommandHandler("monstergpt", monstergpt_handler),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
    )

    application.add_handler(conv_handler)
    job_queue = application.job_queue

    # UTC time!
    monster_monday = job_queue.run_daily(monster_monday_reminder, time(8, 30), (1,))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
