#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Lucas Costa Campos <rmk236@gmail.com>
#
# Distributed under terms of the MIT license.

import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import logging

import database.database as db

TOKEN = os.environ["BOT_TOKEN"]
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Function to decide the starting conditions
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# Make line uppercase
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def register(update, context):
    zip_code = context.args[0]
    chat_id = update.effective_chat.id
    db.add_person(zip_code, chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Added you, with zip code {}".format(zip_code))

# Just repeat message
def echo(update, context):
    reply_markup = telegram.ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm back.", reply_markup=reply_markup)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Allow for the caps on inline mode
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def request_location(update, context):
    contact_keyboard = telegram.KeyboardButton(text="Send my contact", request_contact=True)
    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    custom_keyboard = [[ location_keyboard, contact_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                      text="Would you mind sharing your location and contact with me?",
                      reply_markup=reply_markup)

# Handle unknown commands
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Register initial function
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()

# Register "/caps" command
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# Register "/register" command
loc_handler = CommandHandler('register', register)
dispatcher.add_handler(loc_handler)

# Register inline command (called Caps)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

# Register simple echo
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Register unknown message handler. NOTE: This *must* be the last command to be
# registered. Otherwise, the following registered comamnds will not be
# recognized
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
