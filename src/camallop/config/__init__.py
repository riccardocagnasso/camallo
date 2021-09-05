# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""

import os
import configparser
import distutils
from distutils import util
import pytimeparse

from appdirs import user_data_dir


ACCOUNT_PREFIX = "account:"
DEFAULT_INTERVAL = '1h'


class ConfigurationException(Exception):
    pass


class Account(object):
    def __init__(
        self,
        name,
        server,
        username,
        location,
        password=None,
        port=None,
        ssl=True
    ):
        self.name = name
        self.server = server
        self.username = username
        self.location = location
        self.password = password
        self.port = port
        self.ssl = ssl

    def __iter__(self):
        yield 'name', self.name
        yield 'server', self.server
        yield 'username', self.username
        yield 'location', self.location
        yield 'password', self.password
        yield 'port', self.port
        yield 'ssl', self.ssl


class Config(object):
    def __init__(
        self,
        db_file=None,
        storage_folder=None,
        interval=None,
        accounts=[]
    ):

        if db_file is None:
            self.db_file = os.path.join(
                user_data_dir('camallo'),
                'db.json'
            )
        else:
            self.db_file = db_file

        if storage_folder is None:
            self.db_file = os.path.join(
                user_data_dir('camallo'),
                'data'
            )
        else:
            self.storage_folder = storage_folder

        if not interval:
            interval = DEFAULT_INTERVAL

        self.interval = pytimeparse.parse(interval)

        self.accounts = accounts

    @classmethod
    def from_file(cls, path):
        config = configparser.ConfigParser()

        config.read(path)

        db_file = None
        storage_folder = None
        interval = None
        accounts = []

        if 'main' in config:
            main = config['main']

            db_file = main.get('db_file')
            storage_folder = main.get('storage_folder')
            interval = main.get('interval')

        for s in config.sections():
            if s.startswith(ACCOUNT_PREFIX):
                name = s[len(ACCOUNT_PREFIX):]
                section = config[s]

                if 'server' not in section:
                    raise ConfigurationException(
                        "Account {} has no server".format(name)
                    )

                if 'username' not in section:
                    raise ConfigurationException(
                        "Account {} has no username".format(name)
                    )

                location = section.get('location')

                if not location:
                    self.db_file = os.path.join(
                        user_data_dir('camallo'),
                        'data',
                        name
                    )

                ssl = section.get('ssl')

                if not ssl:
                    ssl = False
                else:
                    ssl = util.strtobool(ssl)

                accounts.append(Account(
                    name=name,
                    server=section.get('server'),
                    username=section.get('username'),
                    location=section.get('location'),
                    password=section.get('password'),
                    port=section.get('port'),
                    ssl=ssl
                ))
        return Config(
            db_file,
            storage_folder,
            interval,
            accounts
        )

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_directories(self):
        self.create_dir(os.path.dirname(self.db_file))
        self.create_dir(self.storage_folder)

        for a in self.accounts:
            self.create_dir(a.location)

    def __iter__(self):
        yield 'db_file', self.db_file
        yield 'storage_folder', self.storage_folder
        yield 'interval', self.interval

        for a in self.accounts:
            yield a.name, dict(a)
