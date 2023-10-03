from dotenv import load_dotenv
import os
import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InputMediaPhoto
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
from datetime import time, timezone
import random

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
SPECIAL_USERS = [int(os.getenv("MASTER_USER"))]


async def security_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text(
            "Hey! You are not allowed to use me! 🚨🚓"
        )
        raise ApplicationHandlerStop


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    greetings = [
        "Greetings! 🎨 What kind of fluffy monster would you like to create today?",
        "Hello there! 🌟 Ready to bring your unique fluffy monster to life? 🧸",
        "Hey, fantastic monster enthusiast! 🤗 What whimsical creature are you planning to design? 🎉",
        "Welcome! 🚀 Tell me, what's your vision for the perfect fluffy monster? 🌈",
        "Hi! 🌼 What adorable and fluffy abomination shall we craft together? 🪄",
        "Greetings, monster magician! 🪄 What delightful fluffy monster is on your mind? 🌟",
        "Hello, creative monster mastermind! 🌈 What's your imaginative monster idea for today? 🤔",
        "Hey there, fluffy monster aficionado! 🐻 What kind of cuddly chaos are we diving into today? 🎈",
        "Welcome, monster maestro! 🎨 Describe your fluffy monster masterpiece-to-be! 🎉",
        "Hi, monster maven! 🌟 What fluffy, adorable creation can I help you bring to life today? 🤗",
    ]
    await update.message.reply_text(random.choice(greetings))

    bubble_examples = [
        "Here's an example: Two happy fluffy monsters are singing in the rain. 🌧️",
        "Let me tell you an example: A cute baby monster with a red balloon. 🎈",
        "Here's an example: A happy fluffy monster is watering a monstera plant. 🪴",
        "Imagine this: A red happy fluffy monster is riding a cargo bike. 🚲",
        "Picture this scene: A happy fluffy monster is dancing on a rainbow. 🌈",
        "How about this: Two happy fluffy monsters riding a tram. 🚋",
        "Here's a creative idea: A happy fluffy monster painting a vibrant masterpiece. 🎨",
        "Consider this scenario: A group of happy fluffy monsters enjoying a sunny day at the park. ☀️🌳",
        "Here's a fun image: A mischievous baby monster playing with a giant lollipop. 🍭",
        "Picture this: A happy fluffy monster family picnicking in a meadow. 🧺🍓",
        "Visualize this adventure: Two adventurous happy fluffy monsters on a mountain hike. ⛰️🌲",
        "Imagine the joy: A friendly red happy fluffy monster delivering smiles on a scooter. 🛵",
        "Let's dive into this scene: A happy fluffy monster surfing the waves at the beach. 🌊🏄",
        "Listen to the music: A talented happy fluffy monster playing a grand piano. 🎹🎶",
        "Here's a magical journey: Two happy fluffy monsters exploring a magical forest. 🌳🌟",
    ]
    await update.message.reply_text(random.choice(bubble_examples))

    lazy_variations = [
        "Feeling a bit lazy? 😅 No worries, just enter /monstergpt and let the magic happen! 🪄",
        "Need a shortcut? 😎 You can simply type /monstergpt and watch the fun unfold! 🚀",
        "Short on time? 🕒 No problem at all—enter /monstergpt and enjoy the monster-making experience! 🎨",
        "Don't want to type it all out? 😌 Just use /monstergpt and let the fluffy monster creation begin! 🌈",
        "In a hurry? 🏃‍♂️ No sweat! Type /monstergpt, and we'll take care of the rest! 🎉",
        "If you're feeling a tad lazy today, that's okay! 😄 Simply enter /monstergpt and let's get started! 🧸",
        "Lazy day? 🛋️ No problemo! Use /monstergpt, and we'll handle the fluffy monster crafting for you! 🪄",
        "Want to keep it simple? 😌 Just enter /monstergpt and let the monster-making adventure begin! 🚲",
        "Feeling a bit relaxed today? 🌴 No sweat! Enter /monstergpt and let's create some fluffy magic! ✨",
        "Don't want to overcomplicate things? 😅 Just use /monstergpt, and we'll do the rest! 🎈",
    ]

    await update.message.reply_text(random.choice(lazy_variations))

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

    await update.message.reply_text(
        "Save your favourite image and post it to Instagram 🆙"
    )

    caption = (
        context.user_data.get("prompt")
        + "\n\n#happyfluffymonsters #monster #digitalart #dalle #openai #aiart #opensea #nft #blockchain #cryptoart"
    )

    await update.message.reply_text(caption)


async def monstergpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "Alrighty it's time for MONSTERGPT.\n\nLet me think about a prompt for a second ... 💬"
    )

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(
        f'Okay, here you go: "{context.user_data.get("prompt")}" 😻\n\nNow I will let DALLE-2 generate some Images ... 🖼️'
    )

    await send_proposal(update, context)

    await update.message.reply_text(
        "Bye! Click /rerun if you are not happy with my generated art 😿"
    )

    context.user_data.clear()

    return ConversationHandler.END


async def monstergpt_rerun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text("So... you are unhappy!??? 😾 \n\nLet me think... 💬")

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(
        f'How about: "{context.user_data.get("prompt")}" 😻\n\nImage generation in process ... 🖼️'
    )

    await send_proposal(update, context)

    await update.message.reply_text(
        "Still unhappy? Well, you know what to do ... /rerun 🙀\nOtherwise, bye!"
    )

    context.user_data.clear()

    return ConversationHandler.END


async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["prompt"] = update.message.text

    await update.message.reply_text(
        "Perfect ✨ I'll ask dalle to create some images. This will take some time. Relax for a bit 💆"
    )

    await send_proposal(update, context)

    await update.message.reply_text("Bye! 😸")

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    await update.message.reply_text(
        "Bye! I hope we can talk again some day 😿", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def monster_monday_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=SPECIAL_USERS[0], text="It's monster monday!!🙀"
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

    # application.add_handler(CommandHandler('monstergpt', monstergpt))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
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
