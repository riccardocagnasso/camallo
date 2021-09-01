# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""


class Worker(object):
    def __init__(self, imaps, db):
        self.imaps = imaps
        self.db = db

    def process_imap(self):
        imap = self.imaps[0]

        messages = imap.get_messages_list()

        for m in messages:
            if self.db.check_message(imap.username, m['uid']):
                print("MESSAGE ALREADY IN", imap.username, m['uid'])
            else:
                self.save_message(imap.username, m)

    def save_message(self, username, m):
        print("SAVE MESSAGE", username, m['uid'])
        self.db.add_message(username, m['uid'])
