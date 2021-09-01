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

from camallop import *
from camallop.imap import *
from camallop.worker import *

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import TinyDB

from camallop.db import *
from appdirs import user_data_dir


@click.command()
@click.option('--username', type=click.STRING)
@click.option('--password', type=click.STRING)
@click.option('--db', type=click.Path())
@click.argument('server', type=click.STRING)
def main(
        username,
        password,
        server,
        db
):
    if db is None:
        db = user_data_dir('camallo')

    print("DB", db)

    storage = TinyDB(
        db,
        storage=CachingMiddleware(JSONStorage)
    )

    db = MessagesDB(storage)

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


if __name__ == "__main__":
    main()
