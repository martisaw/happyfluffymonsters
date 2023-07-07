import logging
import os
from dotenv import load_dotenv

import openaiwrapper

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# load_dotenv('./hfm.env') done in other file...

from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ApplicationHandlerStop, TypeHandler

SPECIAL_USERS = [int(os.getenv('MASTER_USER'))]  # Allows users

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in SPECIAL_USERS:
        pass
    else:
        await update.effective_message.reply_text("Hey! You are not allowed to use me!")
        raise ApplicationHandlerStop
    
async def monsters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Let's do that.")
    prompt = ' '.join(context.args)
    
    image_list = openaiwrapper.create_images(prompt)

    media_list = []
    for image in image_list:
        media_list.append(InputMediaPhoto(media=image['url']))
    
    meta_media_group = await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_list)
    # logging.info(meta_media_group[0])

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enjoy!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    handler = TypeHandler(Update, callback) # Making a handler for the type Update
    application.add_handler(handler, -1) # Default is 0, so we are giving it a number below 0

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler('start', start)
    monsters_handler = CommandHandler('monsters', monsters)
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(echo_handler)
    application.add_handler(monsters_handler)
    
    application.run_polling()
    