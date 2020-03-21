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
import queue

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
            self.counter += 1
            if self.counter % 3 == 0:
                logging.info("Adding new request")
                db.request_DB.add_request(98798273, "123")

            time.sleep(5)
            logging.info("Checking for news")
            requests = db.request_DB.get_requests()
            logging.info(f"Found {len(requests)} new requests")

            # Try to sort the current requests
            for request in requests:
                try:
                    chat_id = request.assigned_chat
                    self.bot.send_message(chat_id=chat_id, text=f"A new request! You can choose to accept it with /accept {request.id_number}, or to reject it /reject {request.id_number}")
                # If you don't work, then go back into the queueu
                    db.request_DB.mark_request(request.id_number, "PENDING")
                except:
                    pass

    def register_callbacks(self):

        # Register "/register" command
        self.reg_handler = CommandHandler('register', self.new_user)
        self.dispatcher.add_handler(self.reg_handler)

        # Register "/accept" command
        self.accept_handler = CommandHandler('accept', self.accept_request)
        self.dispatcher.add_handler(self.accept_handler)

        # Register "/register" command
        self.reject_handler = CommandHandler('reject', self.reject_request)
        self.dispatcher.add_handler(self.reject_handler)

        # Register "/fulfill" command
        self.fulfill_handler = CommandHandler('fulfill', self.fulfill_request)
        self.dispatcher.add_handler(self.fulfill_handler)

        # Register unknown message handler. NOTE: This *must* be the last command to be
        # registered. Otherwise, the following registered comamnds will not be
        # recognized
        self.unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(self.unknown_handler)

    def new_user(self, update, context):
        zip_code = context.args[0]
        chat_id = update.effective_chat.id
        db.volunteer_DB.add_person(zip_code, chat_id)
        logging.info(f"Added user with ZIP code {zip_code} and chat_id {chat_id}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Added you, with zip code {}".format(zip_code))

    def accept_request(self, update, context):
        request_id = context.args[0]
        chat_id = update.effective_chat.id
        if db.request_DB.check_user_asignment(request_id, chat_id):

            request = db.request_DB.get_request_with_id(request_id)
            context.bot.send_message(chat_id=chat_id, text=f"Thank you for accepting the request! You can call {request.phone_number}")
            db.request_DB.mark_request(request_id, "ACCEPTED")
        else:
            context.bot.send_message(chat_id=chat_id, text=f"Sorry, but we could not recognize the request with that ID. Could you double check?")

    def fulfill_request(self, update, context):
        request_id = context.args[0]
        chat_id = update.effective_chat.id
        if db.request_DB.check_user_asignment(request_id, chat_id):

            request = db.request_DB.get_request_with_id(request_id)
            context.bot.send_message(chat_id=chat_id, text=f"Thank you! Marking this request as fulfilled!")
            db.request_DB.mark_request(request_id, "FULFILLED")
        else:
            context.bot.send_message(chat_id=chat_id, text=f"Sorry, but we could not recognize the request with that ID. Could you double check?")

    def reject_request(self, update, context):
        request_id = context.args[0]
        chat_id = update.effective_chat.id

        if db.request_DB.check_user_asignment(request_id, chat_id):
            request = db.request_DB.get_request_with_id(request_id)
            context.bot.send_message(chat_id=chat_id, text=f"It is a pity you can't help now :(. See you later!")
            db.request_DB.mark_request(request_id, "OPEN")
        else:
            context.bot.send_message(chat_id=chat_id, text=f"Sorry, but we could not recognize the request with that ID. Could you double check?")

    # Handle unknown commands
    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    bot = Bot()

if __name__ == "__main__":
    main()
