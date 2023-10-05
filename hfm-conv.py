from dotenv import load_dotenv
import os
import logging
import os
import json
from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    TypeHandler,
    ApplicationHandlerStop,
)
from openaiwrapper import OpenAiWrapper, OpenAiWrapperMock
from datetime import time
import random
from static_messages import (
    start_greetings,
    start_examples,
    start_monstergpt,
    monstergpt_greetings,
    monstergpt_dalle,
    monstergpt_bye,
    monstergpt_rerun_greetings,
    monstergpt_rerun_dalle,
    monstergpt_rerun_bye,
    prompt_dalle,
    prompt_bye,
    cancel_bye,
    monster_monday_reminder_greetings,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# TODO Move file functionality to differen file :)
image_folder_path = "img"
if not os.path.exists(image_folder_path):
    os.makedirs(image_folder_path)

# Load all environment variables
load_dotenv("./hfm.env")

if os.getenv("DEV_MODE") == "yes":
    logger.info("***** running in DEV mode *****")
    openaiwrapper = OpenAiWrapperMock()

else:
    logger.info("***** running in PROD mode *****!")
    openaiwrapper = OpenAiWrapper(os.getenv("OPENAI_API_KEY"), 4, 1024)

PROMPT = range(1)

# Only allows predefined users
SPECIAL_USERS = json.loads(os.getenv("MASTER_USER_ARRAY"))


async def security_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.name in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text(
            "Hey! You are not allowed to use me! 🚨🚓"
        )
        raise ApplicationHandlerStop


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    await update.message.reply_text(random.choice(start_greetings))

    await update.message.reply_text(random.choice(start_examples))

    await update.message.reply_text(random.choice(start_monstergpt))

    return PROMPT


async def image_proposal(image_list):
    count = 1
    media_list = []
    for image in image_list:
        caption = "#" + str(count)
        media_list.append(InputMediaPhoto(media=image["url"], caption=caption))
        count = count + 1
    return media_list


async def send_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_list = openaiwrapper.create_images(context.user_data.get("prompt"))

    context.user_data["media_list"] = await image_proposal(image_list)

    await update.message.reply_media_group(media=context.user_data.get("media_list"))

    instagram_post_variations = [
        "Save your favorite image and post it to Instagram for the world to see! 📸🌍",
        "Don't forget to save your favorite image and share it on Instagram! 📷📤",
        "Capture the moment: Save your favorite image and upload it to Instagram! 📸🌟",
        "Time to show off your creativity: Save your favorite image and post it on Instagram! 🎨📷",
        "Share the magic: Save your favorite image and let it shine on Instagram! ✨📤",
        "Your masterpiece deserves the spotlight: Save it and post on Instagram! 🌟📸",
        "Save that precious image and share it with your Instagram followers! 📸📤",
        "Make your art Instagram-worthy: Save your favorite image and post it! 🎨📷",
        "Don't keep it to yourself: Save your favorite image and share it on Instagram! 🌈📤",
        "It's time for an Instagram moment: Save and post your favorite image! 📸🌟",
    ]

    await update.message.reply_text(random.choice(instagram_post_variations))

    caption = (
        context.user_data.get("prompt")
        + "\n\n#happyfluffymonsters #monster #digitalart #dalle #openai #aiart #opensea #nft #blockchain #cryptoart"
    )

    await update.message.reply_text(caption)


async def monstergpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(random.choice(monstergpt_greetings))

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(f'"{context.user_data.get("prompt")}" 😻')

    await update.message.reply_text(random.choice(monstergpt_dalle))

    await send_proposal(update, context)

    await update.message.reply_text(random.choice(monstergpt_bye))

    context.user_data.clear()

    return ConversationHandler.END


async def monstergpt_rerun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(random.choice(monstergpt_rerun_greetings))

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(f'"{context.user_data.get("prompt")}" 😻\n\n')

    await update.message.reply_text(random.choice(monstergpt_rerun_dalle))

    await send_proposal(update, context)

    await update.message.reply_text(random.choice(monstergpt_rerun_bye))

    context.user_data.clear()

    return ConversationHandler.END


async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["prompt"] = update.message.text
    await update.message.reply_text(random.choice(prompt_dalle))

    await send_proposal(update, context)

    await update.message.reply_text(random.choice(prompt_bye))

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    await update.message.reply_text(random.choice(cancel_bye))

    return ConversationHandler.END


async def monster_monday_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=SPECIAL_USERS[0], text=random.choice(monster_monday_reminder_greetings)
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("TOKEN")).build()
    handler = TypeHandler(
        Update, security_callback
    )  # Making a handler for the type Update
    application.add_handler(
        handler, -1
    )  # Default is 0, so we are giving it a number below 0

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("monster", start),
            CommandHandler("start", start),
            CommandHandler("monstergpt", monstergpt),
            CommandHandler("rerun", monstergpt_rerun),
        ],
        states={
            PROMPT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, prompt),
                CommandHandler("monstergpt", monstergpt),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    job_queue = application.job_queue

    # UTC time!
    monster_monday = job_queue.run_daily(monster_monday_reminder, time(8, 30), (1,))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
