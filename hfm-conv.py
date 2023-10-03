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

    monstergpt_variations = [
        "Alrighty, it's time for MONSTERGPT! 🎉 Let me think about a prompt for a second... 🤔",
        "Get ready for MONSTERGPT! 🚀 Let's brainstorm a prompt for a moment... 💭",
        "It's MONSTERGPT time! 🧟‍♂️ Give me a sec to come up with a prompt... ⏳",
        "Time for some MONSTERGPT magic! ✨ Let me ponder a prompt for a second... 💡",
        "MONSTERGPT is here! 🦄 Just need a moment to conjure up a prompt... 🪄",
        "MONSTERGPT time has arrived! 🌟 Let's mull over a prompt for a sec... 🤓",
        "Get excited for MONSTERGPT! 🎈 I'm brewing a prompt idea for a moment... ☕",
        "MONSTERGPT is on the scene! 🌈 Give me a brief moment to think of a prompt... 🤗",
        "Ready for some MONSTERGPT action! 🎨 Just need a quick second for a prompt... ⏱️",
        "MONSTERGPT is in the house! 🏡 Let me brainstorm a prompt for a moment... 💭",
    ]

    await update.message.reply_text(random.choice(monstergpt_variations))

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(f'"{context.user_data.get("prompt")}" 😻')

    dalle_variations = [
        "Now, it's time to let DALL·E-2 work its magic! 🖼️✨",
        "Let's unleash DALL·E-2 for some creative image generation! 🎨🌟",
        "Prepare for image wonderment as DALL·E-2 takes the stage! 📷🪄",
        "It's DALL·E-2's time to shine and craft stunning images! 🌆🚀",
        "Watch in awe as DALL·E-2 brings images to life! 🌄🌠",
        "DALL·E-2 is here to dazzle with its image-making prowess! 🌅📸",
        "Ready for a visual treat? DALL·E-2 is set to create captivating images! 🎆🖼️",
        "Let DALL·E-2 work its artistic magic and produce marvelous images! 🖌️🌈",
        "DALL·E-2 is on the scene for some incredible image generation! 🌃🎨",
        "Get ready to be amazed as DALL·E-2 crafts beautiful images! 🌌📷",
    ]

    await update.message.reply_text(random.choice(dalle_variations))

    await send_proposal(update, context)

    bye_variations = [
        "Goodbye for now! 👋 Click /rerun if you're not thrilled with my art. 🎨",
        "Farewell! 😊 If my art didn't quite hit the mark, just hit /rerun. 🖼️",
        "Take care! 🌟 Don't forget, you can always click /rerun for more art. 🎭",
        "Until next time! 🚀 If my creation isn't your cup of tea, use /rerun. ☕",
        "So long! 🎨 Feel free to tap /rerun if you want another art piece. 🖌️",
        "Goodbye, art enthusiast! 🖼️ Remember, there's /rerun for more masterpieces. 🖋️",
        "Adieu! 🌈 If my art didn't quite capture your imagination, try /rerun. 🧙‍♂️",
        "Fare thee well! 🌄 You can always hit /rerun for a fresh art experience. 🎆",
        "See you later! 📸 If my art isn't your style, just click /rerun. 📷",
        "Bye for now! 🖌️ Don't hesitate to use /rerun if you want something different. 🚀",
    ]

    await update.message.reply_text(random.choice(bye_variations))

    context.user_data.clear()

    return ConversationHandler.END


async def monstergpt_rerun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    unhappy_variations = [
        "Oh no! 😟 You're not happy with my created pictures!??? Let me put on my thinking cap... 🤔",
        "Hmm, it seems my art didn't quite hit the mark, huh? 😕 Let me think of a better idea... 🖌️",
        "I see you're not thrilled with my creations! 😞 No worries, let me brainstorm something new... 🧠",
        "Not satisfied with my pictures, huh? 😔 Don't fret, I'll come up with something better... 🌟",
        "Feeling a bit disappointed in my creations? 😢 Let me ponder and improve... 🎨",
        "Oh dear, you're not quite happy with what I made. 😥 Let me put on my creativity hat... 🎩",
        "It seems I missed the mark with my pictures, didn't I? 😓 Let me think of a better approach... 🖼️",
        "Don't worry! 😄 If my creations didn't meet your expectations, I'll come up with something better... 🚀",
        "Unhappy with my art? 😞 I'm on it! Let me think of ways to make it right... 🤓",
        "Not quite what you had in mind, huh? 😕 No problem, let me think and create something better... 🌈",
    ]

    await update.message.reply_text(random.choice(unhappy_variations))

    context.user_data["prompt"] = openaiwrapper.create_randomized_prompt()

    await update.message.reply_text(f'"{context.user_data.get("prompt")}" 😻\n\n')

    generation_variations = [
        "Image generation in progress... 🖼️✨",
        "Creating images as we speak... 🎨🌟",
        "Generating images as you wait... 📷🚀",
        "Artwork in the making... 🌆🖌️",
        "Pictures coming to life... 🌈📸",
        "Crafting images for you... 🧙‍♂️🖼️",
        "Watch the magic unfold... 🪄📷",
        "Image generation underway... 🚧✨",
        "Creating visual wonders... 🌟🎨",
        "Art in progress... 🖌️🌄",
    ]

    await update.message.reply_text(random.choice(generation_variations))

    await send_proposal(update, context)

    unhappy_with_art_variations = [
        "Still unhappy with my art? 😞 Well, you know what to do ... /rerun. Otherwise, bye! 👋",
        "Not quite satisfied with my art? 😔 Don't hesitate to use /rerun. If not, then bye! 👋",
        "Feeling disappointed in my art? 😢 Remember, you can always hit /rerun. If not, farewell! 👋",
        "Art didn't meet your expectations? 😕 Just type /rerun. If not, take care and goodbye! 👋",
        "Unhappy with the art I created? 😟 Use /rerun if you want more. If not, it's time to say goodbye! 👋",
        "If my art didn't quite hit the mark, no worries! 😓 Just tap /rerun. If not, farewell! 👋",
        "Not thrilled with my art? 😖 You have the magic word: /rerun. If not, goodbye! 👋",
        "Still not loving my art? 😣 Don't forget about /rerun. Otherwise, it's time to bid adieu! 👋",
        "Artistic disappointment? 😭 Use /rerun for a fresh start. If not, take care and goodbye! 👋",
        "Art not up to par? 😩 Type /rerun to try again. If not, it's time to say farewell! 👋",
    ]

    await update.message.reply_text(random.choice(unhappy_with_art_variations))

    context.user_data.clear()

    return ConversationHandler.END


async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["prompt"] = update.message.text
    dalle_image_generation_variations = [
        "Perfect! 🌟 I'll ask DALL·E to work its magic and create some images. This will take some time. 🎨 Relax for a bit. 😌",
        "Great choice! 👍 I'm enlisting DALL·E to craft some images. It'll take a while. 🖼️ Take a breather. 🌬️",
        "Wonderful! 🙌 I'm summoning DALL·E to weave its artistry and generate images. Patience is key. ⏳ Take a break. 🍃",
        "Excellent decision! 💡 I'll request DALL·E to conjure up some images. It might be a bit. 📸 Take a moment to unwind. 🌄",
        "Fantastic! 🚀 DALL·E is on the case to create images. It'll take some time. 🎨 Relax and recharge. 💆‍♂️",
        "Brilliant! ✨ DALL·E will craft images for you. It's a bit of a wait. 🌆 Take a moment to decompress. 🍵",
        "Splendid! 🌈 I'm calling upon DALL·E for image creation. It'll be worth it. 🖼️ Take a short break. 🏖️",
        "Perfect choice! 🎉 DALL·E is at your service to generate images. Be patient. 📸 Relax for a bit. 🛋️",
        "Awesome! 🌟 I'm tasking DALL·E to make some images. It takes time. 🎨 Take a breather. ☕",
        "Terrific! 👏 DALL·E is on the job for image creation. It requires a little wait. 📷 Take a break. 🌿",
    ]

    await update.message.reply_text(random.choice(dalle_image_generation_variations))

    await send_proposal(update, context)

    goodbye_variations = [
        "Bye! 👋",
        "Farewell! 🌟",
        "See you later! 🚀",
        "Take care! 😊",
        "Goodbye and take care! 🌈",
        "Till we meet again! 👋🌄",
        "Adieu! 🌟",
        "Catch you later! 🚀",
        "So long! 😎",
        "Until next time! 🌸",
    ]

    await update.message.reply_text(random.choice(goodbye_variations))

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    canceled_variations = [
        "Canceled! 😞 I hope we can talk again someday! 🌟",
        "Oops, it's canceled! 😅 Let's hope for another chat someday! 🌈",
        "Unfortunately canceled! 😔 But fingers crossed for a future conversation! 🤞",
        "Canceled, but not forever! 😊 Looking forward to chatting again someday! 🚀",
        "It's a cancel today, but let's stay hopeful for future talks! 🙏😌",
        "Canceled for now! 🌆 Hoping to catch up again someday soon! 📆",
        "Don't worry, it's just a cancel! 😅 We'll chat again someday! 🌟",
        "Canceled this time, but there's always hope for future discussions! 🌄🤞",
        "Oops, it got canceled! 😓 Let's plan for a chat in the future! 🚀",
        "Canceled, but the conversation door is always open! 🚪😊",
    ]

    await update.message.reply_text(random.choice(canceled_variations))

    return ConversationHandler.END


async def monster_monday_reminder(context: ContextTypes.DEFAULT_TYPE):
    monster_monday_variations = [
        "It's monster Monday!! 🎉👹",
        "Happy monster Monday! 🌟👾",
        "Guess what day it is? It's monster Monday!! 🎈👹",
        "Welcome to monster Monday! 🚀👻",
        "Monster Monday has arrived! 🌄👾",
        "Get ready for some monster fun—it's Monday! 🎉👹",
        "Monster Monday vibes! 🌟👻",
        "Embrace the monster in you—it's Monday! 🚀👾",
        "Monday means monsters! 🌈👹",
        "Let's conquer this monster of a Monday! 💪👻",
    ]

    await context.bot.send_message(
        chat_id=SPECIAL_USERS[0], text=random.choice(monster_monday_variations)
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
