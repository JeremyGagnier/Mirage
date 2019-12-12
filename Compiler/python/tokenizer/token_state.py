from enum import Enum

class TokenState:
    values = []

Enum.value(TokenState, "COMMENT")
Enum.value(TokenState, "ESCAPED")
Enum.value(TokenState, "FLOAT")
Enum.value(TokenState, "INT")
Enum.value(TokenState, "INT_DOT")
Enum.value(TokenState, "INT_DOT_ERROR")
Enum.value(TokenState, "NAME")
Enum.value(TokenState, "NAME_ERROR")
Enum.value(TokenState, "NUMBER_ERROR")
Enum.value(TokenState, "STRING")
Enum.value(TokenState, "SYMBOL")
Enum.value(TokenState, "SYMBOL_ERROR")
Enum.value(TokenState, "WHITESPACE")
