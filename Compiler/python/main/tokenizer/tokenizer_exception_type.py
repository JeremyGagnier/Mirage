from mirage_enum import Enum

class TokenizerExceptionType:
    values = []

Enum.value(TokenizerExceptionType, "BAD_CHAR_IN_NAME", "{0}:{1} bad character when parsing name: {2}")
Enum.value(TokenizerExceptionType, "BAD_CHAR_IN_NUMBER", "{0}:{1} bad character when parsing number: {2}")
Enum.value(TokenizerExceptionType, "BAD_CHAR_IN_SYMBOL", "{0}:{1} bad character when parsing symbol: {2}")
Enum.value(TokenizerExceptionType, "STRING_NOT_TERMINATED", "{0}:{1} string not terminated")
Enum.value(TokenizerExceptionType, "UNEXPECTED_DOT", "{0}:{1} bad character after number with dot: {2}")
Enum.value(TokenizerExceptionType, "UNKNOWN_SYMBOL", "{0}:{1} unknown symbol found: {2}")
