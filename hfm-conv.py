import logging
import os
# openaiwrapper load environment file ... FIXME

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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

from openaiwrapper1 import OpenAiWrapper

openaiwrapper = OpenAiWrapper()

PROMPT, SELECT, SUMMARY = range(3)

# Temporary Variables for saving context
tmp_prompt = None
tmp_media_list = []
tmp_select = None
image_list = [
    {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simple_Stick_Figure.svg/170px-Simple_Stick_Figure.svg.png'},
    {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simple_Stick_Figure.svg/170px-Simple_Stick_Figure.svg.png'}
] # filled with data for mocking!

def clean_variables():
    global tmp_prompt
    global tmp_media_list
    global tmp_select
    global image_list
    tmp_prompt = None
    tmp_media_list = []
    tmp_select = None
    image_list = [
        {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simple_Stick_Figure.svg/170px-Simple_Stick_Figure.svg.png'},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simple_Stick_Figure.svg/170px-Simple_Stick_Figure.svg.png'}
    ] # filled with data for mocking!

SPECIAL_USERS = [int(os.getenv('MASTER_USER'))]  # Allows users

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text("Hey! You are not allowed to use me!")
        raise ApplicationHandlerStop

async def monstergpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clean_variables()

    await update.message.reply_text('running fully automated mode')
    auto_prompt = openaiwrapper.create_randomized_prompt()
    await update.message.reply_text(f'generated prompt: {auto_prompt}')
    image_list = openaiwrapper.create_images(auto_prompt) # local
    
    count = 1
    reply_list = []
    for image in image_list:
        caption = '#' + str(count)
        tmp_media_list.append(InputMediaPhoto(media=image['url'], caption=caption))
        reply_list.append(caption)
        count = count + 1
    
    await update.message.reply_media_group(media=tmp_media_list)
    await update.message.reply_text('done. enjoy.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    clean_variables()

    await update.message.reply_text(
        'Hey there! I\'m Bubbles 🫧, your happy fluffy monster creator. \n\nLet\'s generate happy fluffy monsters 👹. \n\nWhat are my peers doing today?' 
    )

    return PROMPT

async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tmp_prompt 
    global tmp_media_list
    tmp_prompt = update.message.text

    await update.message.reply_text(
        'Perfect ✨ I\'ll ask dalle to create some images. This will take some time. Relax for a bit 💆'
    )
    # The next line will talk to openai!
    image_list = openaiwrapper.create_images(tmp_prompt)
    
    count = 1
    reply_list = []
    for image in image_list:
        caption = '#' + str(count)
        tmp_media_list.append(InputMediaPhoto(media=image['url'], caption=caption))
        reply_list.append(caption)
        count = count + 1
    
    await update.message.reply_media_group(media=tmp_media_list)
    
    reply_keyboard = [reply_list]

    await update.message.reply_text(
        'Which one would you like to post on Instagram? \n\nYou can /skip this.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    
    return SELECT

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global tmp_select
    tmp_select = update.message.text
    tmp_url = None
    for media_item in tmp_media_list:
        if media_item.caption == tmp_select:
            tmp_url = media_item.media
    caption = tmp_prompt + '\n\n #happyfluffymonsters#digitalart'
    await update.message.reply_text('All done. Please review the following instagram post 🕵️')
    await update.message.reply_photo(photo=tmp_url, caption=caption) # FIXME Two times downloading the picture?
    await update.message.reply_text('Send /post if you want to post on instagram or /cancel this.')

    return SUMMARY

async def skip_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('alright, skipped - see ya 🤓')
    return ConversationHandler.END

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('sorry, not yet implemented 😿 bye!')
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TOKEN')).build()
    handler = TypeHandler(Update, callback) # Making a handler for the type Update
    application.add_handler(handler, -1) # Default is 0, so we are giving it a number below 0
    
    application.add_handler(CommandHandler('monstergpt', monstergpt))
   
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PROMPT:[MessageHandler(filters.TEXT & ~filters.COMMAND, prompt)],
            SELECT:[
                CommandHandler('skip', skip_select),
                MessageHandler(filters.TEXT & ~filters.COMMAND, select)# filters.TEXT to unprecise!
            ], 
            SUMMARY: [CommandHandler('post', summary)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()