# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""


import configparser


class Account(object):
    


class Config(object):
    def __init__(
        self,
        db_file,
        storage_folder,
        accounts
    ):
        self.db_file = db_file
        self.storage_folder = storage_folder
        self.accounts = accounts
