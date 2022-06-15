from typing import List, Dict, Union

from . import types

Lexemes = List["Lexeme"]
Tokens = List["Token"]
Context = Dict[str, Union[int, callable]]
TokenValue = Union[float, str, Tokens, "FuncCall"]


class Lexeme:
    """
    A class that contains a raw piece of input stream.
    It may be: number, literal, operator, lbrace, rbrace
    """

    def __init__(self, typeof: types.LexemeType, value: str):
        self.type = typeof
        self.value = value

    def __str__(self):
        return f"Lexeme(type={self.type.name}, value={repr(self.value)})"

    __repr__ = __str__


class Token:
    def __init__(self,
                 kind: types.TokenKind,
                 typeof: types.TokenType,
                 value: TokenValue,
                 ):
        self.kind = kind
        self.type = typeof
        self.value = value

    def __str__(self):
        return f"Token(kind={self.kind.name}, type={self.type.name}, value={repr(self.value)})"

    __repr__ = __str__


class FuncCall:
    """
    This class is just a container for func call details.
    Supposed to be kept in Token as a value
    """

    def __init__(self, name: str, args: List[Tokens]):
        self.name = name
        self.args = args

    def __str__(self):
        return f"FuncCall(name={repr(self.name)}, args={repr(self.args)})"

    __repr__ = __str__
