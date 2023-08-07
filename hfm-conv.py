DEV = True

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

from openaiwrapper1 import OpenAiWrapper, OpenAiWrapperMock
from instawrapper import InstaWrapper, InstaWrapperMock

if DEV is not True:
    openaiwrapper = OpenAiWrapper(4, 1024)
    instawrapper = InstaWrapper()
else:
    openaiwrapper = OpenAiWrapperMock()
    instawrapper = InstaWrapperMock()

PROMPT, SELECT, SUMMARY = range(3)

# Only allows predefined users
SPECIAL_USERS = [int(os.getenv('MASTER_USER'))]

# Security
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text("Hey! You are not allowed to use me! 🚨🚓")
        raise ApplicationHandlerStop

async def monstergpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text('🤖 ... running fully automated mode.\n\nGenerating prompt 💬')

    context.user_data['prompt'] = openaiwrapper.create_randomized_prompt()
    await update.message.reply_text(f'🤖 ... generated prompt: {context.user_data.get("prompt")}\n\nGenerating Images 🖼️')
    
    image_list = openaiwrapper.create_images(context.user_data.get('prompt'))
    
    media_and_keyboard = await image_proposal(image_list)

    context.user_data['media_list'] = media_and_keyboard[0]
    reply_keyboard = media_and_keyboard[1]
    
    await update.message.reply_media_group(media=context.user_data.get('media_list'))

    await update.message.reply_text(
        'Which one would you like to post on Instagram? \n\nYou can /cancel this.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return SELECT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()

    await update.message.reply_text(
        'Hey there! I\'m Bubbles 🫧, your happy fluffy monster creator. \n\nLet\'s generate happy fluffy monsters 👹. \n\nWhat are my peers doing today?' 
    )

    return PROMPT

async def image_proposal(image_list) -> ():

    count = 1
    reply_list = []
    media_list = []
    for image in image_list:
        caption = '#' + str(count)
        media_list.append(InputMediaPhoto(media=image['url'], caption=caption))
        reply_list.append(caption)
        count = count + 1
    
    reply_keyboard = [reply_list]

    # overwrite reply_keyboard if more than two (formatting)
    if len(reply_list) > 2:
        chunked_reply_list = []
        chunk_size = 2

        for i in range(0, len(reply_list), chunk_size):
            chunked_reply_list.append(reply_list[i:i+chunk_size])

        reply_keyboard = chunked_reply_list

    return (media_list, reply_keyboard)

async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    context.user_data['prompt'] = update.message.text

    await update.message.reply_text(
        'Perfect ✨ I\'ll ask dalle to create some images. This will take some time. Relax for a bit 💆'
    )
    # The next line will talk to openai!
    image_list = openaiwrapper.create_images(context.user_data.get('prompt'))
    
    media_and_keyboard = await image_proposal(image_list)

    context.user_data['media_list'] = media_and_keyboard[0]
    reply_keyboard = media_and_keyboard[1]

    await update.message.reply_media_group(media=context.user_data['media_list'])
    
    await update.message.reply_text(
        'Which one would you like to post on Instagram? \n\nYou can /cancel this.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    
    return SELECT

async def reselect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    await update.message.reply_text(
        'Choose again.'
    )
    
    count = 1
    reply_list = []
    for image in context.user_data['media_list']:
        caption = '#' + str(count)
        reply_list.append(caption)
        count = count + 1
    
    await update.message.reply_media_group(media=context.user_data['media_list'])
    
    reply_keyboard = [reply_list]

    await update.message.reply_text(
        'Which one would you like to post on Instagram? \n\nYou can /cancel this.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    
    return SELECT

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    tmp_select = update.message.text
    tmp_url = None
    for media_item in context.user_data.get('media_list'):
        if media_item.caption == tmp_select:
            tmp_url = media_item.media
    caption = context.user_data.get('prompt') + '\n\n#happyfluffymonsters #monster #digitalart #dalle #openai #aiart #opensea #nft #blockchain #cryptoart'
    await update.message.reply_text('All done. Please review the following instagram post 🕵️')
    sent_message = await update.message.reply_photo(photo=tmp_url, caption=caption) # FIXME Two times downloading the picture?
    await update.message.reply_text('Send /post if you want to post on instagram, /reselect to choose another image or /cancel this.')
    
    # Move the code below to the final function -> In case of reselect this is overwritten
    sent_photo = await sent_message.photo[-1].get_file()
    file_name = context.user_data.get('prompt').replace(" ", "_") 
    if file_name.endswith('.'):
        file_name = file_name + "jpg"
    else:
        file_name = file_name + ".jpg"
    file_path = await sent_photo.download_to_drive(file_name)
    context.user_data['ig_photo']=file_path
    context.user_data['ig_caption']=caption
    ######

    return SUMMARY

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    await update.message.reply_text('⚙️ processing ...')
    instawrapper.upload_photo(context.user_data.get('ig_photo'), context.user_data.get('ig_caption'))
    await update.message.reply_text('Posted! See ya next time 😻')
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    context.user_data.clear()
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
    
    # application.add_handler(CommandHandler('monstergpt', monstergpt))
   
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler('monstergpt', monstergpt)],
        states={
            PROMPT:[MessageHandler(filters.TEXT & ~filters.COMMAND, prompt)],
            SELECT:[MessageHandler(filters.TEXT & ~filters.COMMAND, select)# filters.TEXT to unprecise!
                    ], 
            SUMMARY: [CommandHandler('reselect', reselect), CommandHandler('post', summary)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()