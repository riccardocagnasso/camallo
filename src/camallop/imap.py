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
import pprint


class IMAPReader(object):
    def __init__(
        self,
        address,
        port=imaplib.IMAP4_SSL_PORT,
        username=None,
        password=None
    ):
        self.imap = imaplib.IMAP4_SSL(address, port)

        if username and password:
            self.imap.login(username, password)

        status, messages = self.imap.select("INBOX")
        N = 3
        messages = int(messages[0])

        print("STATUS", status, "MESSSAGES", messages)
