# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""


from setuptools import setup, find_packages

setup(
    name="camallo",
    version="0.1",
    packages=find_packages('src/camallo'),
    package_dir={'': 'src'},
    author="Riccardo Cagnasso",
    author_email="riccardo@musiquarium.it",
    license="WTFPL",
    include_package_data=True,
    keywords="python email imap backup",
    scripts=[
        'src/scripts/camallo.py'
    ],
    install_requires=[
        'click',
        'lark-parser',
        'tinydb'
    ]
)
