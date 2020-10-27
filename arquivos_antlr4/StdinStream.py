import codecs
import sys

from antlr4.InputStream import InputStream


class StdinStream(InputStream):
    def __init__(self, encoding:str='utf-8', errors:str='replace') -> None:
        bytes = sys.stdin.buffer.read()
        data = codecs.decode(bytes, encoding, errors)
        super().__init__(data)
