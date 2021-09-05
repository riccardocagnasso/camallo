# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""

import imaplib

from camallop.parsers.uid import *


class IMAPAdapter(object):
    @classmethod
    def factory(cls, account):
        if account.ssl:
            return SSLAUTHIMAP(
                account.server,
                account.port,
                account.username,
                account.password
            )
        else:
            raise NotImplementedError()


class SSLAUTHIMAP(object):
    def __init__(
        self,
        server,
        port,
        username,
        password
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        self.imap = imaplib.IMAP4_SSL(self.server, self.port)
        self.imap.login(
            self.username,
            self.password
        )

    def disconnect(self):
        self.imap.close()
        self.imap.logout()


class IMAPReader(object):
    def __init__(
        self,
        imap_adapter,
    ):
        self.uid_parser = UIDParser()
        self.imap_adapter = imap_adapter

    def connect(self):
        self.imap_adapter.connect()

    def disconnect(self):
        self.imap_adapter.disconnect()

    def get_messages_list(self):
        messages = []

        self.imap_adapter.imap.select("INBOX", readonly=True)
        resp, data = self.imap_adapter.imap.uid('FETCH', '1:*', '(UID)')

        for message in data:
            message = message.decode('utf-8')
            m_id, m_uid = self.uid_parser.parse(message)

            messages.append({
                'id': m_id,
                'uid': m_uid
            })

        return messages

    def fetch_message(self, i):

        self.imap_adapter.imap.select("INBOX", readonly=True)

        status, m = self.imap_adapter.imap.fetch(str(i), "(RFC822)")

        return m
