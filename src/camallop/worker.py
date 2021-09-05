# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""
from camallop.imap import *

import os


class Worker(object):
    def __init__(self, accounts, db):
        self.accounts = accounts
        self.db = db

    def process_account(self):
        account = self.accounts[0]

        imap_reader = IMAPReader(IMAPAdapter.factory(account))

        imap_reader.connect()

        for m in imap_reader.get_messages_list():
            if self.db.check_message(account.name, m['uid']):
                print("MESSAGE ALREADY IN", account.name, m['uid'])
            else:
                self.save_message(account, m, imap_reader)

        imap_reader.disconnect()
        self.db.flush()

    def save_message(self, account, m, imap_reader):
        print("SAVE MESSAGE", account.name, m['uid'])
        self.db.add_message(account.name, m['uid'])

        message = imap_reader.fetch_message(m['id'])

        filename = os.path.join(
            account.location,
            m['uid'] + '.eml'
        )

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        f = open(filename, 'wb')
        f.write(message[0][1])
        f.close()
