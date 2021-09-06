#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
At first all used functions are defined, the main function at the last of the file.

Usage:
Example of a telegram-user using the bot:
Starts the bot by sending /start, then proceeds to translation via the /translate
command, get asked for the destination language and text to tranlate, then a translation 
o the sent text is sent to the user. 
"""

import logging
from constants import API_TOKEN
import translate_main

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# List of available languages  
reply_keyboard = translate_main.list_languages()

markup = ReplyKeyboardMarkup(([language] for language in reply_keyboard), one_time_keyboard=True)


def receive_translation(text) -> str:
    """Access the translation API"""
    dest_lang = dest_language.lower()
    untranslated_text = text
    translated_text = translate_main.do_translation(dest_lang, untranslated_text)
    
    return translated_text


def start(update: Update, context: CallbackContext) -> None:
    """Start the conversation and ask user for input."""
    # Say Hey

    if update.message.from_user['username'] != None:
        update.message.reply_text(f"Hey, @{update.message.from_user['username']} !")
    elif update.message.from_user['username'] == None and update.message.from_user['first_name'] != None:
        update.message.reply_text(f"Hey, {update.message.from_user['first_name']} !")
    else:
        update.message.reply_text("Hey there!")

    # Give info about the bot 
    update.message.reply_text(
        "Hercules - Translate is a language translation bot that is currently under development.\
        \n\nUse the Menu button to get started, or use /help.\
        \n\nIf you encounter any errors, please feel free to give feedback for the developer, use /developer."
    )


def translate(update: Update, context: CallbackContext) -> int:
    """Start handling translation"""
    update.message.reply_text(
        "Choose a langauge to translate to (destination language):",
        reply_markup=markup,
    )
    
    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    global dest_language
    dest_language = update.message.text
    update.message.reply_text(
        f'Okay, send me the text you want to translate to {dest_language.capitalize()}:'
    )

    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    text = update.message.text

    update.message.reply_text(
        f"{receive_translation(dest_language)}: {receive_translation(text)}"
    )
    
    return ConversationHandler.END


def done(update: Update, context: CallbackContext) -> None:
    """End conversation"""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    
    update.message.reply_text(
        "Okay, done!",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    user_data.clear()
    return ConversationHandler.END


def list_langs(update: Update, context: CallbackContext) -> None:
    """Sends a message with all available languages for translation"""
    string_ = ''
    for language in translate_main.list_languages():
        if  translate_main.list_languages().index(language) != len(translate_main.list_languages()) - 1:
            string_ += f"{language}, "
        else:
            string_ += f"{language}."
            
    update.message.reply_text(
        string_
    )


def developer(update: Update, context: CallbackContext) -> None:
    """Sends a message with information about the developer"""
    update.message.reply_text(
        "I am a young developer from Addis Ababa, Ethiopia.\
        \nI am honestly not very experienced with what I do, but I do it with a grip to succeeding in it.\
        \n\nHere are some ways to contact me \
        \n<a href='https://www.linkedin.com/in/tariq-hamid/'>LinkedIn</a>\
        \n<a href='https://github.com/tariq-hamid'>GitHub</a>\
        \n<a href='https://www.instagram.com/tariq8.6/'>Instagram</a> :P\
        \nYou can also contact me here @diifuso\
        \n\nHercules is an open-source bot, I would like to expand it furthur in the services it offers. I mean not just translation.\
        \nAnd Hercules is in need of more developers to develop it. If interested, contact me ASAP!!!",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


def help_(update: Update, context: CallbackContext) -> None:
    """Send a message with information about the bot"""
    update.message.reply_text(
        "You can use this bot for in-telegram text translation, this bot is based on Google Translate api.\
        \n\nTo view all available language for the translation service, use /list_languages\
        \n\nTo translate a text, use /translate. Then:\
        \n1. Send the destination Language\
        \n2. Send the text you want to translate. You don't have to specify the language of the text you sent, that wll be detected by the bot.\
        \n3. That's it, the bot will send you the translation.\
        \n\nAll commands:\
        \n/translate\
        \n/list_languages\
        \n/developer\
        \n/help",
        parse_mode=ParseMode.HTML
    )


def detect(update: Update, context: CallbackContext, text) -> None:
    """Uses the language of text"""
    

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # /start handler
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Add conversation handler for /translate with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    translate_handler = ConversationHandler(
        entry_points=[CommandHandler('translate', translate)],
        states={
            CHOOSING: [
                MessageHandler(
                    (Filters.text & (~Filters.command)), regular_choice
                )
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command),
                    received_information,
                )
            ],
        },
        
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )
    dispatcher.add_handler(translate_handler)
    
    # /list_langs handler
    list_langs_handler = CommandHandler('list_languages', list_langs)
    dispatcher.add_handler(list_langs_handler)
    
    # /detect handler
    detect_handler = CommandHandler('detect', detect)
    dispatcher.add_handler(detect_handler)
    
    # /developer
    developer_handler = CommandHandler('developer', developer)
    dispatcher.add_handler(developer_handler)
    
    # /help
    help_handler = CommandHandler('help', help_)
    dispatcher.add_handler(help_handler)
    
    
    # Start the Bot
    updater.start_webhook(listen='0.0.0.0',
                         port=8443,
                         url_path=API_TOKEN,
                         key='private.key',
                         cert='cert.pem',
                         webhook_url=f'https://b1qp84.deta.dev/:8443/{API_TOKEN}')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()