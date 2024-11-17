from handlers.conversation_static import *
from service.chat_service import generate_random_prompt
from service.image_service import (
    generate_styled_images,
    generate_image_proposal,
)
import random
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

PROMPT = range(1)


async def _send_proposal(
    update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str
):
    image_list = generate_styled_images(prompt)

    if len(image_list) == 0:
        await update.message.reply_text("could not generate images 😪")
    else:
        await update.message.reply_media_group(
            await generate_image_proposal(prompt, image_list)
        )

        await update.message.reply_text(random.choice(send_proposal_insta))

        caption = (
            prompt
            + "\n\n#happyfluffymonsters #monster #digitalart #dalle #openai #aiart #opensea #nft #blockchain #cryptoart"
        )

        await update.message.reply_text(caption)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(random.choice(start_greetings))

    await update.message.reply_text(random.choice(start_examples))

    await update.message.reply_text(random.choice(start_monstergpt))

    return PROMPT


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(random.choice(cancel_bye))

    return ConversationHandler.END


async def monstergpt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(monstergpt_greetings))

    prompt = generate_random_prompt()

    await update.message.reply_text(f'"{prompt}" 😻')

    await update.message.reply_text(random.choice(monstergpt_dalle))

    await _send_proposal(update, context, prompt)

    await update.message.reply_text(random.choice(monstergpt_bye))

    return ConversationHandler.END


async def rerun_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(monstergpt_rerun_greetings))

    prompt = generate_random_prompt()

    await update.message.reply_text(f'"{prompt}" 😻\n\n')

    await update.message.reply_text(random.choice(monstergpt_rerun_dalle))

    await _send_proposal(update, context, prompt)

    await update.message.reply_text(random.choice(monstergpt_rerun_bye))

    return ConversationHandler.END


async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(random.choice(prompt_dalle))

    await _send_proposal(update, context, update.message.text)

    await update.message.reply_text(random.choice(prompt_bye))

    return ConversationHandler.END
