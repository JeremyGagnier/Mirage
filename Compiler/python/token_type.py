from enum import Enum

_TOKEN_NAME_TO_SYMBOLS = {
    "OPEN_ARGUMENT": ["("],
    "CLOSE_ARGUMENT": [")"],
    "OPEN_CODE": ["{"],
    "CLOSE_CODE": ["}"],
    "OPEN_TEMPLATE": ["["],
    "CLOSE_TEMPLATE": ["]"],
    "NEWLINE": ["\n"],
    "COMMA": [","],
    "DOT": ["."],
    "CLASS": ["class"],
    "OBJECT": ["object"],
    "ENUM": ["enum"],
    "IF": ["if"],
    "ELSE": ["else"],
    "EQUALS": ["=", "+=", "-=", "*=", "/="],
    "PUBLIC": ["public"],
    "PRIVATE": ["private"],
    "PROTECTED": ["protected"],
    "VAR": ["var"],
    "METHOD_MOD": ["override", "abstract"],
    "PACKAGE": ["package"],
    "IMPORT": ["import"],
    "THROW": ["throw"],
    "IN": ["in"],
    "TEST": ["test"],
    "COLON": [":"],
    "SLASH": ["/"],
    "DASH": ["-"],
    "FLOAT": [],
    "INT": [],
    "STRING": [],
    "NAME": [],
    "BIN_OP": ["+", "*", "^", ">", "<", "<=", ">=", "!=", "and", "or", "mod"],
    "UNI_OP": ["not"],
    "PIPE": ["|"]}

_SYMBOL_TO_TOKEN_NAMES = {}


class TokenType:
    values = []


    @staticmethod
    def contains(symbol):
        return symbol in _SYMBOL_TO_TOKEN_NAMES


    @staticmethod
    def get(symbol):
        return _SYMBOL_TO_TOKEN_NAMES[symbol]


# Fill the TokenType class
for (token_name, symbols) in _TOKEN_NAME_TO_SYMBOLS.items():
    Enum.value(TokenType, token_name, symbols)

# Build the inverted map. There should not be duplicates in the symbols because the token parser is not powerful enough
# to determine what token type is correct in that case. Duplicates should be consolidated to a new token type that gets
# resolved by the grammar.
for (token_name, symbols) in _TOKEN_NAME_TO_SYMBOLS.items():
    for symbol in symbols:
        _SYMBOL_TO_TOKEN_NAMES[symbol] = vars(TokenType)[token_name]


TokenType.LINE_START_TOKENS = [
    TokenType.CLASS,
    TokenType.OBJECT,
    TokenType.ENUM,
    TokenType.PUBLIC,
    TokenType.PRIVATE,
    TokenType.PROTECTED,
    TokenType.VAR,
    TokenType.METHOD_MOD,
    TokenType.PACKAGE,
    TokenType.IMPORT,
    TokenType.THROW,
    TokenType.TEST,
    TokenType.FLOAT,
    TokenType.INT,
    TokenType.STRING,
    TokenType.NAME]