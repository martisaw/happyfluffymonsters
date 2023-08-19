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
    ApplicationHandlerStop
)
from openaiwrapper import OpenAiWrapper, OpenAiWrapperMock
from datetime import time, timezone

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
load_dotenv('./hfm.env')

if os.getenv('DEV_MODE') == 'yes':
    logger.info("***** running in DEV mode *****")
    openaiwrapper = OpenAiWrapperMock()
    
else:
    logger.info("***** running in PROD mode *****!")
    openaiwrapper = OpenAiWrapper(os.getenv('OPENAI_API_KEY'), 4, 1024)

PROMPT = range(1)

# Only allows predefined users
SPECIAL_USERS = [int(os.getenv('MASTER_USER'))]

async def security_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text("Hey! You are not allowed to use me! 🚨🚓")
        raise ApplicationHandlerStop

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    await update.message.reply_text(
        'Hey there! I\'m Bubbles 🫧, your happy fluffy monster creator.\n\nWhat are my peers doing today?\n\nAn example: "A happy fluffy monster dances in the rain."' 
    )

    await update.message.reply_text(
        'Also, if you are lazy: just enter /monstergpt 😎' 
    )

    return PROMPT

async def image_proposal(image_list):

    count = 1
    media_list = []
    for image in image_list:
        caption = '#' + str(count)
        media_list.append(InputMediaPhoto(media=image['url'], caption=caption))
        count = count + 1
    return media_list

async def send_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_list = openaiwrapper.create_images(context.user_data.get('prompt'))

    context.user_data['media_list'] = await image_proposal(image_list)
    
    await update.message.reply_media_group(media=context.user_data.get('media_list'))

    await update.message.reply_text("Save your favourite image and post it to Instagram 🆙")

    caption = context.user_data.get('prompt') + '\n\n#happyfluffymonsters #monster #digitalart #dalle #openai #aiart #opensea #nft #blockchain #cryptoart'
    
    await update.message.reply_text(caption)

async def monstergpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text("Alrighty it's time for MONSTERGPT.\n\nLet me think about a prompt for a second ... 💬")

    context.user_data['prompt'] = openaiwrapper.create_randomized_prompt()
    
    await update.message.reply_text(f'Okay, here you go: "{context.user_data.get("prompt")}" 😻\n\nNow I will let DALLE-2 generate some Images ... 🖼️')
    
    await send_proposal(update, context)

    await update.message.reply_text("Bye! Click /rerun if you are not happy with my generated art 😿")

    context.user_data.clear()

    return ConversationHandler.END

async def monstergpt_rerun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text("So... you are unhappy!??? 😾 \n\nLet me think... 💬")

    context.user_data['prompt'] = openaiwrapper.create_randomized_prompt()
    
    await update.message.reply_text(f'How about: "{context.user_data.get("prompt")}" 😻\n\nImage generation in process ... 🖼️')
    
    await send_proposal(update, context)

    await update.message.reply_text("Still unhappy? Well, you know what to do ... /rerun 🙀\nOtherwise, bye!")

    context.user_data.clear()

    return ConversationHandler.END

async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    context.user_data['prompt'] = update.message.text

    await update.message.reply_text(
        'Perfect ✨ I\'ll ask dalle to create some images. This will take some time. Relax for a bit 💆'
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
    await context.bot.send_message(chat_id=SPECIAL_USERS[0], text="It's monster monday!!🙀")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TOKEN')).build()
    handler = TypeHandler(Update, security_callback) # Making a handler for the type Update
    application.add_handler(handler, -1) # Default is 0, so we are giving it a number below 0
    
    # application.add_handler(CommandHandler('monstergpt', monstergpt))
   
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("monster", start), CommandHandler("start", start), CommandHandler('monstergpt', monstergpt), CommandHandler('rerun', monstergpt_rerun)],
        states={
            PROMPT:[MessageHandler(filters.TEXT & ~filters.COMMAND, prompt), CommandHandler('monstergpt', monstergpt)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    job_queue = application.job_queue

    # UTC time!
    monster_monday = job_queue.run_daily(monster_monday_reminder, time(8,30), (1,))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()