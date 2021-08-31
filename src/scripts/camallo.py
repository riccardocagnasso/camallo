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


@click.command()
@click.option('--username', type=click.STRING)
@click.option('--password', type=click.STRING)
@click.argument('server', type=click.STRING)
def main(
        username,
        password,
        server
):
    imap = IMAPReader(
        server,
        username=username,
        password=password
    )


if __name__ == "__main__":
    main()
