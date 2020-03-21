#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Lucas Costa Campos <rmk236@gmail.com>
#
# Distributed under terms of the MIT license.

from enum import Enum
import logging

# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
class Volunteer(object):

    """Docstring for Volunteer. """

    def __init__(self, chat_id, zip_code): 
        """TODO: to be defined.

        :chat_id: TODO
        :zip_code: TODO

        """
        self.chat_id = chat_id
        self.zip_code = zip_code


class Volunteers(object):

    """Docstring for Volunteers. """

    def __init__(self):
        """TODO: to be defined. """
        self.volunteers = []

    def add_person(self, zip_code, chat_id):
        self.volunteers.append(Volunteer(chat_id, zip_code))

    def find_person(self, zip_code):
        for v in self.volunteers:
            if v.zip_code == zip_code:
                return v
        return None

class Request(object):

    """Docstring for Request. """

    def __init__(self, phone_number, zip_code, id_number, assigned_chat):
        """TODO: to be defined.

        :phone_number: TODO
        :zip_code: TODO
        :id_number: TODO

        """
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.id_number = id_number
        self.assigned_chat = assigned_chat
        self.status = "OPEN"


class Requests(object):

    """Docstring for Requests. """

    def __init__(self):
        """TODO: to be defined. """
        self.requests = []
        self.count = 0

    def add_request(self, phone_number, zip_code):
        volunteers = volunteer_DB.find_person(zip_code)
        new_request = Request(phone_number, zip_code, str(self.count), volunteers.chat_id)
        self.requests.append(new_request)
        self.count += 1

    def get_requests(self):
        requests = [request for request in self.requests if request.status == "OPEN"]
        return requests

    def check_user_asignment(self, request_id, chat_id):
        for request in self.requests:
            if request.assigned_chat == chat_id and request.id_number == request_id:
                return True
        return False

    def get_request_with_id(self, request_id):
        logging.info(f"Looking for ID {request_id}")
        for request in self.requests:
            if request.id_number == request_id:
                logging.info("Found ID!")
                return request
        logging.info("ID not found!")
        # return [request for request in self.requests if request.id_number == request_id][0]

    def mark_request(self, request_id, status):
        for idx, request in enumerate(self.requests):
            if request.id_number == request_id:
                self.requests[idx].status = status

volunteer_DB = Volunteers()
request_DB = Requests()
