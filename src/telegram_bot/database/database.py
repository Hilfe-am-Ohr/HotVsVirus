#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Lucas Costa Campos <rmk236@gmail.com>
#
# Distributed under terms of the MIT license.


chat_ids = []
zip_codes = []

def add_person(zip_code, chat_id):
    chat_ids.append(chat_id)
    zip_codes.append(zip_code)

def find_person(zip_code):
    return chat_ids[zip_codes.index(zip_code)]
