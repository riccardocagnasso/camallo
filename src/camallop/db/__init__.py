# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""
from tinydb import Query


class MessagesDB(object):
    def __init__(self, storage):
        self.db = storage

    def add_message(self, account, uid):
        self.db.insert({
            'account': account,
            'uid': uid
        })

    def check_message(self, account, uid):
        Message = Query()

        ret = self.db.search(
            (Message.account == account) & (Message.uid == uid)
        )

        return len(ret) > 0

    def flush(self):
        self.db.storage.flush()
