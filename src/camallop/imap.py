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
        print("START")
        self.uid_parser = UIDParser()

        self.imap = imaplib.IMAP4_SSL(address, port)

        if username and password:
            self.imap.login(username, password)

        status, messages = self.imap.select("INBOX", readonly=True)
        messages = int(messages[0])

        print("STATUS", status, "MESSSAGES", messages)

        resp, data = self.imap.uid('FETCH', '1:*', '(UID)')
        # self.imap.fetch('1:*', "(ID,UID)")

        for message in data:
            message = message.decode('utf-8')
            m_id, m_uid = self.uid_parser.parse(message)

            print("MESSAGE", m_id, m_uid)

        self.imap.close()
        self.imap.logout()
