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


class IMAPReader(object):
    def __init__(
        self,
        address,
        port=imaplib.IMAP4_SSL_PORT,
        username=None,
        password=None
    ):
        self.uid_parser = UIDParser()
        self.imap = imaplib.IMAP4_SSL(address, port)

        self.username = username
        self.password = password

        if self.username and self.password:
            self.imap.login(
                self.username,
                self.password
            )

    def get_messages_list(self):
        messages = []

        self.imap.select("INBOX", readonly=True)
        resp, data = self.imap.uid('FETCH', '1:*', '(UID)')

        for message in data:
            message = message.decode('utf-8')
            m_id, m_uid = self.uid_parser.parse(message)

            messages.append({
                'id': m_id,
                'uid': m_uid
            })

        return messages

    def fetch_message(self, i):

        self.imap.select("INBOX", readonly=True)

        status, m = self.imap.fetch(str(i), "(RFC822)")

        print("STATUS", status)
        print("M", m[0][1])

        f = open('out.eml', 'wb')
        f.write(m[0][1])
        f.close()

    def close(self):
        self.imap.logout()
        self.imap.close()
