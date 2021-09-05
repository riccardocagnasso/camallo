# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""
import click
import os

from camallop import *
from camallop.imap import *
from camallop.worker import *
from camallop.config import *

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import TinyDB

from camallop.db import *
from appdirs import user_data_dir


@click.command()
@click.option('--config', type=click.Path())
def main(
        config
):
    if config is None:
        config = os.path.join(
            user_data_dir('camallo'),
            'config.ini'
        )

    config = Config.from_file(config)
    config.create_directories()

    import pprint
    pprint.pp(dict(config))

    storage = TinyDB(
        config.db_file,
        storage=CachingMiddleware(JSONStorage)
    )

    db = MessagesDB(storage)
    worker = Worker(
        config.accounts,
        db
    )

    worker.process_account()
    """

    imap = IMAPReader(
        server,
        username=username,
        password=password
    )

    worker = Worker(
        [imap],
        db
    )

    # worker.process_imap()
    # storage.close()

    imap.fetch_message(1)
    """


if __name__ == "__main__":
    main()
