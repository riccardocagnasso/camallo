# -*- coding: utf-8 -*-
"""
Copyright © 2021 Riccardo Cagnasso <riccardo@phascode.org>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ for more details.
"""


from lark import Lark, Transformer

grammar = """
start: message
message: INT "(UID " INT ")"
%import common.INT
%ignore " "
"""


class UIDTransformer(Transformer):
    def message(self, matches):
        return (matches[0].value, matches[1].value)

    def start(self, matches):
        return matches[0]


class UIDParser(object):
    def __init__(self):
        self.parser = Lark(grammar)
        self.transformer = UIDTransformer()

    def parse(self, str):
        str = str.replace('\n', '')
        tree = self.transformer.transform(self.parser.parse(str))
        return tree
