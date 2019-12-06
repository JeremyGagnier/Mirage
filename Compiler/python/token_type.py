class TokenType:
    OPEN_ARGUMENT = "OPEN_ARGUMENT"
    CLOSE_ARGUMENT = "CLOSE_ARGUMENT"
    OPEN_CODE = "OPEN_CODE"
    CLOSE_CODE = "CLOSE_CODE"
    OPEN_TEMPLATE = "OPEN_TEMPLATE"
    CLOSE_TEMPLATE = "CLOSE_TEMPLATE"
    NEWLINE = "NEWLINE"
    COMMA = "COMMA"
    DOT = "DOT"
    CLASS = "CLASS"
    OBJECT = "OBJECT"
    ENUM = "ENUM"
    IF = "IF"
    ELSE = "ELSE"
    EQUALS = "EQUALS"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    PROTECTED = "PROTECTED"
    VAR = "VAR"
    METHOD_MOD = "METHOD_MOD"
    LOOP = "LOOP"
    PACKAGE = "PACKAGE"
    IMPORT = "IMPORT"
    THROW = "THROW"
    BREAK = "BREAK"
    IN = "IN"
    TEST = "TEST"
    COLON = "COLON"
    SLASH = "SLASH"
    DASH = "DASH"
    FLOAT = "FLOAT"
    INT = "INT"
    STRING = "STRING"
    NAME = "NAME"
    BIN_OP = "BIN_OP"
    UNI_OP = "UNI_OP"

    TOKEN_TYPE_TO_SYMBOLS = {
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
        "LOOP": ["loop"],
        "PACKAGE": ["package"],
        "IMPORT": ["import"],
        "THROW": ["throw"],
        "BREAK": ["break"],
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
        "UNI_OP": ["not"]}

    SYMBOL_TO_TOKEN_TYPES = {}
    for (token_type, tokens) in TOKEN_TYPE_TO_SYMBOLS.items():
        for token in tokens:
            SYMBOL_TO_TOKEN_TYPES[token] = token_type

    def get(token_string):
        TokenType.SYMBOL_TO_TOKEN_TYPES[token_string]
