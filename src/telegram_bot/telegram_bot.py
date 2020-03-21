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
import time
import os

import database.database as db

# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

class Bot(object):

    """Docstring for Bot. """

    def __init__(self):
        """TODO: to be defined. """
        # Start the bot
        logging.debug("Reading token")
        TOKEN = os.environ["BOT_TOKEN"]
        logging.info("Starting bot")
        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.updater.start_polling()
        logging.info("Successful start!")

        self.counter = 0


        logging.info("Registering callbacks!")
        self.register_callbacks()

        while True:
            logging.info("Checking for news")
            requests = self.fetch_news()
            logging.info(f"Found {len(requests)} new requests")

            for request in requests:
                zip_code = request["zip_code"]
                logging.debug(f"Processing request for zip_code {zip_code}")
                chat_id = db.find_person(zip_code)
                logging.debug(f"Found a good sould at {zip_code} with chat_id {chat_id}")

                phone_number = request["phone_number"]

                logging.info(f"Sending message to {chat_id}")
                self.bot.send_message(chat_id=chat_id, text=f"New request! Please call {phone_number}!")



    def fetch_news(self):
        time.sleep(5)

        self.counter += 1
        if self.counter%5 == 0:
            return [
                {"zip_code": str(123),
                 "phone_number": 1766878,
                 "request_id": self.counter
                 }
            ]

        return []

    def register_callbacks(self):

        # Register "/register" command
        self.reg_handler = CommandHandler('register', self.new_user)
        self.dispatcher.add_handler(self.reg_handler)

        # Register unknown message handler. NOTE: This *must* be the last command to be
        # registered. Otherwise, the following registered comamnds will not be
        # recognized
        self.unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(self.unknown_handler)

    def new_user(self, update, context):
        zip_code = context.args[0]
        chat_id = update.effective_chat.id
        db.add_person(zip_code, chat_id)
        logging.info(f"Added user with ZIP code {zip_code} and chat_id {chat_id}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Added you, with zip code {}".format(zip_code))

    # Handle unknown commands
    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    bot = Bot()

if __name__ == "__main__":
    main()
