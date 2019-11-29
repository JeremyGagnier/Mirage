NUMBERS = "0123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHANUMERIC = ALPHABET + NUMBERS

SYMBOL = "SYMBOL"
VALUE = "VALUE"
FN_MOD = "FN_MOD"
OP = "OP"
L_PAREN = "L_PAREN"
R_PAREN = "R_PAREN"
L_CURLY = "L_CURLY"
R_CURLY = "R_CURLY"
L_BRACK = "L_BRACK"
R_BRACK = "R_BRACK"
COMMA = "COMMA"
PUB = "PUB"
VAR = "VAR"
DOT = "DOT"
CLASS = "CLASS"
NEWLINE = "NEWLINE"
EQUALS = "EQUALS"
PACKAGE = "PACKAGE"
IMPORT = "IMPORT"
UNIOP = "UNIOP"
THROW = "THROW"
IF = "IF"
LOOP = "LOOP"
BREAK = "BREAK"
IN = "IN"
OBJECT = "OBJECT"
TEST = "TEST"
READABLE = "READABLE"
WHERE = "WHERE"
SHOULD = "SHOULD"
THROWS = "THROWS"

INVALID = "INVALID"

START_OF_LINE_TOKENS = (IMPORT, PACKAGE, VAR, PUB, CLASS, FN_MOD, OBJECT, LOOP, BREAK, THROW, IF, TEST, READABLE)
# Additionally TYPE and FN_DECL count as a start of line tokens but they aren't primitive

class Token:
    def __init__(self, token_str, line_num):
        self.token_str = token_str
        self.line_num = line_num

        # TODO: Figure out how to detect UNIOP
        if token_str == ".":
            self.type = DOT
        elif token_str == "\n":
            self.type = NEWLINE
        elif token_str == ",":
            self.type = COMMA
        elif token_str == "(":
            self.type = L_PAREN
        elif token_str == ")":
            self.type = R_PAREN
        elif token_str == "{":
            self.type = L_CURLY
        elif token_str == "}":
            self.type = R_CURLY
        elif token_str == "[":
            self.type = L_BRACK
        elif token_str == "]":
            self.type = R_BRACK
        elif token_str == "if":
            self.type = IF
        elif token_str == "in":
            self.type = IN
        elif token_str == "pub":
            self.type = PUB
        elif token_str == "var":
            self.type = VAR
        elif token_str == "not":
            self.type = UNIOP
        elif token_str == "null":
            self.type = VALUE
        elif token_str == "test":
            self.type = TEST
        elif token_str == "loop":
            self.type = LOOP
        elif token_str == "break":
            self.type = BREAK
        elif token_str == "throw":
            self.type = THROW
        elif token_str == "class":
            self.type = CLASS
        elif token_str == "where":
            self.type = WHERE
        elif token_str == "import":
            self.type = IMPORT
        elif token_str == "object":
            self.type = OBJECT
        elif token_str == "should":
            self.type = SHOULD
        elif token_str == "throws":
            self.type = THROWS
        elif token_str == "package":
            self.type = PACKAGE
        elif token_str == "readable":
            self.type = READABLE
        elif token_str == "=" or\
             token_str == "+=" or\
             token_str == "-=" or\
             token_str == "*=" or\
             token_str == "/=":
            self.type = EQUALS
        elif (len(token_str) == 1 and token_str in "+-*/^|&<>%") or\
             token_str == "or" or\
             token_str == "and" or\
             token_str == "xor" or\
             token_str == "<=" or\
             token_str == ">=" or\
             token_str == "==":
            self.type = OP
        elif token_str == "abstract" or token_str == "virtual" or token_str == "override":
            self.type = FN_MOD
        else:
            alphanumeric = True
            for char in token_str:
                if char not in ALPHANUMERIC:
                    not_alphanumeric = False
                    break

            if alphanumeric and token_str[0] in ALPHABET:
                self.type = SYMBOL
            else:
                numeric = True
                for char in token_str:
                    if char not in (NUMBERS + "."):
                        numeric = False
                        break

                if numeric and token_str[token_str.find('.') + 1:].find('.') == -1 or token_str[0] == '"' and token_str[-1] == '"':
                    self.type = VALUE
                else:
                    self.type = INVALID

    def __str__(self):
        if self.token_str == "\n":
            token_str = "\\n"
        else:
            token_str = self.token_str
        return self.type + ":" + token_str

    def __repr__(self):
        return self.__str__()
