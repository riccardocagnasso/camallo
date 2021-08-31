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
