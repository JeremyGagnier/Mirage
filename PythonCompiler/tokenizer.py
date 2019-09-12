import string

TOKENIZER_EXCEPTION_STRING = "Error tokenizing file - "
STRING_WAS_NOT_CLOSED_MSG = TOKENIZER_EXCEPTION_STRING + "String at line {0} was not closed."
TOO_MANY_PERIODS_MSG = TOKENIZER_EXCEPTION_STRING + "Value '{0}' on line {1} has too many periods."
NON_NUMBER_MSG = TOKENIZER_EXCEPTION_STRING + "Value '{0}' on line {1} starts with a number but is not a number."
NON_SYMBOL_CHARACTER_MSG = TOKENIZER_EXCEPTION_STRING + "Symbol '{0}' on line {1} has bad characters."

NUMBERS = "0123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOL_CHARACTERS = ALPHABET + NUMBERS + "_"

ADJACENTS = "+-=*/&^%:|<>~!"
ONE_OFFS = "()[]{};,."
COMMENTS = "//"
STRING_CHARACTERS = "\""
NEWLINE = "\n"

STRING_TAG = "\\s"
FLOAT_TAG = "\\f"
INTEGER_TAG = "\\i"
SYMBOL_TAG = "\\o"
NEWLINE_TAG = "\\n"

ENDABLE_TOKENS = ("SYMBOL", "VALUE", "R_PAREN", "R_CURLY")
STARTABLE_TOKENS = ("PUB", "VAR", "READABLE", "SYMBOL", "VALUE", "PACKAGE", "IMPORT", "THROW", "IF", "LOOP", "BREAK", "CLASS", "TEST", "OBJECT", "L_PAREN", "FN_MOD")

class Token:
    def __init__(self, token_str, line_num, grammar):
        self.token_str = token_str
        self.line_num = line_num

        if token_str in grammar.glyphs:
            self.name = grammar.glyphs[token_str]

        else:
            if token_str == NEWLINE:
                self.name = grammar.glyphs[NEWLINE_TAG]
            elif token_str[0] in STRING_CHARACTERS:
                self.name = grammar.glyphs[STRING_TAG]

            elif token_str[0] in NUMBERS:
                is_float = False
                for char in token_str:
                    if char == ".":
                        if is_float:
                            raise Exception(TOO_MANY_PERIODS_MSG.format(token_str, line_num))
                        is_float = True
                    elif char not in NUMBERS:
                        raise Exception(NON_NUMBER_MSG.format(token_str, line_num))
                if is_float:
                    self.name = grammar.glyphs[FLOAT_TAG]
                else:
                    self.name = grammar.glyphs[INTEGER_TAG]

            else:
                for char in token_str:
                    if char not in SYMBOL_CHARACTERS:
                        raise Exception(NON_SYMBOL_CHARACTER_MSG.format(token_str, line_num))
                self.name = grammar.glyphs[SYMBOL_TAG]

    def __str__(self):
        if self.token_str == NEWLINE:
            token_str = "\\n"
        else:
            token_str = self.token_str
        return self.name + ":" + token_str

    def __repr__(self):
        return self.__str__()


class Tokenizer:
    DEBUG = False

    def __init__(self, grammar, code_string):
        self.tokens = []

        if Tokenizer.DEBUG:
            print("Tokenizing code:\n{0}...\n...{1}".format(code_string[:40], code_string[-40:]))

        line_num = 1
        next_token = ""

        def add_token():
            if next_token != "":
                self.tokens.append(Token(next_token, line_num, grammar))

        adjacents = False
        in_string = None
        skip_to_next_line = False
        for char in code_string:
            if skip_to_next_line:
                if char == NEWLINE:
                    skip_to_next_line = False
                    self.tokens.append(Token(NEWLINE, line_num, grammar))
                    line_num += 1
                continue

            if next_token == COMMENTS:
                adjacents = False
                skip_to_next_line = True
                next_token = ""
                continue

            if char in STRING_CHARACTERS:
                adjacents = False
                if in_string == None:
                    in_string = char
                else:
                    if char != in_string:
                        next_token += char
                        add_token()
                        next_token = ""
                        continue

            if not in_string:
                if char == NEWLINE:
                    adjacents = False
                    add_token()
                    self.tokens.append(Token(NEWLINE, line_num, grammar))
                    next_token = ""
                    line_num += 1
                    continue

                if char in string.whitespace:
                    adjacents = False
                    add_token()
                    next_token = ""
                    continue

                if char in ONE_OFFS:
                    adjacents = False
                    add_token()
                    next_token = char
                    add_token()
                    next_token = ""
                    continue

                if not adjacents and char in ADJACENTS:
                    adjacents = True
                    add_token()
                    next_token = ""

                elif adjacents and char not in ADJACENTS:
                    adjacents = False
                    add_token()
                    next_token = ""

            elif next_token == NEWLINE:
                raise Exception(STRING_WAS_NOT_CLOSED_MSG.format(line_num))


            next_token += char

        if in_string:
            raise Exception(STRING_WAS_NOT_CLOSED_MSG.format(line_num))

        if not skip_to_next_line:
            add_token()

        if Tokenizer.DEBUG:
            print("Finished tokenizing. {0} lines, {1} tokens.".format(self.tokens[-1].line_num, len(self.tokens)))

        old_tokens = self.tokens
        self.tokens = []

        for i in range(len(old_tokens) - 1):
            token = old_tokens[i]
            if token.name == "NEWLINE":
                if len(self.tokens) > 0 and self.tokens[-1].name in ENDABLE_TOKENS and old_tokens[i + 1].name in STARTABLE_TOKENS:
                    self.tokens.append(token)
            else:
                self.tokens.append(token)

        if old_tokens[-1].name != "NEWLINE":
            self.tokens.append(old_tokens[-1])

        if Tokenizer.DEBUG:
            print("Finished semicolon inference.")
