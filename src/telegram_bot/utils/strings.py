#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Lucas Costa Campos <rmk236@gmail.com>
#
# Distributed under terms of the MIT license.

class English(object):

    """Docstring for German. """

    def __init__(self):

        self.new_request = "We have a new request! You can choose to accept it with /accept {id_number}, to to reject with /reject {id_number}"
        self.callback_new_user_missing_zip = "Missing ZIP code. Please double check and try again"
        self.callback_new_user_success = "Added you, with ZIP code {zip_code}!"
        self.callback_new_user_error = "Invalid ZIP code! Please double check and try again"

        self.callback_accept_request_missing = "Missing request code. Please try again"
        self.callback_accept_request_success = "Thank you for accepting the request! You can call {phone_number}"
        self.callback_accept_request_error = "Sorry, but we could not recognize the request with that ID. Could you double check?"

        self.callback_reject_request_missing = "Missing request code. Please try again"
        self.callback_reject_request_success = "It is a pity you can't help right now. See you later!"
        self.callback_reject_request_error = "Sorry, but we could not recognize the request with that ID. Could you double check?"

        self.callback_fulfill_request_missing = "Missing request code. Please try again"
        self.callback_fulfill_request_success = "Thank you! Marking this request as fulfilled!"
        self.callback_fulfill_request_error = "Sorry, but we could not recognize the request with that ID. Could you double check?"
