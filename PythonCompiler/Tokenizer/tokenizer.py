from fsm import FSM
from functools import reduce
from token import Token
from token_state import TokenState
from token_type import TokenType
from tokenizer_exception import TokenizerException
from tokenizer_exception_type import TokenizerExceptionType
from tokenizer_state import TokenizerState

_alphabet = "abcdefghijklmnopqrtsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_numbers = "0123456789"
_valid_name_chars = _alphabet + _numbers + "_"
_valid_number_chars = _numbers + "."
_valid_symbol_chars = "()[]{}<>+-*/=,."

_name_starters = _alphabet + "#$"
_number_starters = _numbers
_symbol_starters = _valid_symbol_chars

def whitespace_to_int(char_and_state):
    (char, state) = char_and_state
    return char in _number_starters

def whitespace_to_name(char_and_state):
    (char, state) = char_and_state
    return char in _name_starters

def whitespace_to_string(char_and_state):
    (char, state) = char_and_state
    return char == "\""

def to_whitespace(exception_type, is_invalid_predicate):
    def predicate(char_and_state):
        (char, state) = char_and_state
        if char == "\n" or char == " ":
            return True
        elif (is_invalid_predicate(char)):
            raise TokenizerException(exception_type, state.line_num, state.column_num, char)
        else:
            return False

    return predicate

def comment_to_whitespace(char_and_state):
    (char, state) = char_and_state
    return char == "\n"

def string_to_whitespace(char_and_state):
    (char, state) = char_and_state
    if char == "\"":
        return True
    elif char == "\n":
        raise TokenizerException(TokenizerExceptionType.STRING_NOT_TERMINATED, state.line_num, state.column_num, char)
    else:
        return False

number_to_whitespace = to_whitespace(
    TokenizerExceptionType.BAD_CHAR_IN_NUMBER,
    lambda char: char not in _valid_number_chars)

name_to_whitespace = to_whitespace(
    TokenizerExceptionType.BAD_CHAR_IN_NAME,
    lambda char: char not in _valid_name_chars)

symbol_to_whitespace = to_whitespace(
    TokenizerExceptionType.BAD_CHAR_IN_SYMBOL,
    lambda char: char not in _valid_symbol_chars)

def int_to_int_dot(char_and_state):
    (char, state) = char_and_state
    return char == "."

def int_dot_to_float(char_and_state):
    (char, state) = char_and_state
    return char in _numbers

def int_dot_to_name(char_and_state):
    (char, state) = char_and_state
    return char in _name_starters

def symbol_to_comment(char_and_state):
    (char, state) = char_and_state
    return char == "/" and state.token_text == "/"

def to_symbol(char_and_state):
    (char, state) = char_and_state
    return char in _symbol_starters

def int_to_symbol(char_and_state):
    (char, state) = char_and_state
    return char != "." and char in _symbol_starters

def string_to_escaped(char_and_state):
    (char, state) = char_and_state
    return char == "\\"

def add_char_action(previous_token_state, char_and_tokenizer_state):
    (char, tokenizer_state) = char_and_tokenizer_state
    new_state = TokenizerState(
        tokenizer_state.token_text + char,
        tokenizer_state.token_start_column,
        tokenizer_state.line_num,
        tokenizer_state.column_num + 1)
    return ([], new_state)

def int_dot_error_action(previous_token_state, char_and_tokenizer_state):
    (char, tokenizer_state) = char_and_tokenizer_state
    raise TokenizerException(
        TokenizerExceptionType.UNEXPECTED_DOT,
        tokenizer_state.line_num,
        tokenizer_state.column_num,
        char)

def comment_action(previous_token_state, char_and_tokenizer_state):
    (char, tokenizer_state) = char_and_tokenizer_state
    return ([], tokenizer_state)

def maybe_unpack_token(tokenizer_state, previous_token_state):
    if len(tokenizer_state.token_text) > 0:
        maybe_token_type = None
        if previous_token_state == TokenState.FLOAT:
            maybe_token_type = TokenType.FLOAT
        elif previous_token_state == TokenState.INT:
            maybe_token_type = TokenType.INT
        elif previous_token_state == TokenState.NAME:
            if tokenizer_state.token_text in TokenType.SYMBOL_TO_TOKEN_TYPES:
                maybe_token_type = TokenType.SYMBOL_TO_TOKEN_TYPES[tokenizer_state.token_text]
            else:
                maybe_token_type = TokenType.NAME
        elif previous_token_state == TokenState.STRING:
            maybe_token_type = TokenType.STRING
        elif previous_token_state == TokenState.SYMBOL:
            if tokenizer_state.token_text in TokenType.SYMBOL_TO_TOKEN_TYPES:
                maybe_token_type = TokenType.SYMBOL_TO_TOKEN_TYPES[tokenizer_state.token_text]
            else:
                raise TokenizerException(
                    TokenizerExceptionType.UNKNOWN_SYMBOL,
                    tokenizer_state.line_num,
                    tokenizer_state.column_num,
                    tokenizer_state.token_text)
        
        maybe_token = None
        if maybe_token_type != None:
            maybe_token = Token(
                maybe_token_type,
                tokenizer_state.token_text,
                tokenizer_state.line_num,
                tokenizer_state.column_num)

        new_tokenizer_state = TokenizerState(
            "",
            tokenizer_state.column_num,
            tokenizer_state.line_num,
            tokenizer_state.column_num)

        return (maybe_token, new_tokenizer_state)

    else:
        return (None, tokenizer_state)

def symbol_action(previous_token_state, char_and_tokenizer_state):
    (char, tokenizer_state) = char_and_tokenizer_state
    maybe_token = None
    unpacked_state = tokenizer_state
    if previous_token_state != TokenState.SYMBOL:
        (maybe_token, unpacked_state) = maybe_unpack_token(tokenizer_state, previous_token_state)
    
    new_state = TokenizerState(
        unpacked_state.token_text + char,
        unpacked_state.token_start_column,
        unpacked_state.line_num,
        unpacked_state.column_num + 1)

    token_list = []
    if maybe_token:
        token_list = [maybe_token]

    return (token_list, unpacked_state)

def whitespace_action(previous_token_state, char_and_tokenizer_state):
    (char, tokenizer_state) = char_and_tokenizer_state
    (maybe_token, unpacked_state) = maybe_unpack_token(tokenizer_state, previous_token_state)

    token_list = []
    if maybe_token:
        token_list = [maybe_token]

    new_state = None
    if char == "\n":
        token_list.append(Token(TokenType.NEWLINE, "\\n", unpacked_state.line_num, unpacked_state.column_num))
        new_state = TokenizerState("", unpacked_state.token_start_column, unpacked_state.line_num + 1, 1)
    else:
        new_state = TokenizerState(
            unpacked_state.token_text,
            unpacked_state.token_start_column,
            unpacked_state.line_num,
            unpacked_state.column_num + 1)

    return (token_list, new_state)

_fsm = FSM(TokenState.WHITESPACE)
_fsm.add_state(TokenState.COMMENT, comment_action)
_fsm.add_state(TokenState.ESCAPED, add_char_action)
_fsm.add_state(TokenState.FLOAT, add_char_action)
_fsm.add_state(TokenState.INT, add_char_action)
_fsm.add_state(TokenState.INT_DOT, add_char_action)
_fsm.add_state(TokenState.INT_DOT_ERROR, int_dot_error_action)
_fsm.add_state(TokenState.NAME, add_char_action)
_fsm.add_state(TokenState.STRING, add_char_action)
_fsm.add_state(TokenState.SYMBOL, symbol_action)
_fsm.add_state(TokenState.WHITESPACE, whitespace_action)

_fsm.add_transition(TokenState.WHITESPACE, TokenState.INT, whitespace_to_int)
_fsm.add_transition(TokenState.WHITESPACE, TokenState.NAME, whitespace_to_name)
_fsm.add_transition(TokenState.WHITESPACE, TokenState.STRING, whitespace_to_string)
_fsm.add_transition(TokenState.WHITESPACE, TokenState.SYMBOL, to_symbol)

_fsm.add_transition(TokenState.COMMENT, TokenState.WHITESPACE, comment_to_whitespace)
_fsm.add_transition(TokenState.FLOAT, TokenState.WHITESPACE, number_to_whitespace)
_fsm.add_transition(TokenState.INT, TokenState.WHITESPACE, number_to_whitespace)
_fsm.add_transition(TokenState.NAME, TokenState.WHITESPACE, name_to_whitespace)
_fsm.add_transition(TokenState.STRING, TokenState.WHITESPACE, string_to_whitespace)
_fsm.add_transition(TokenState.SYMBOL, TokenState.WHITESPACE, symbol_to_whitespace)

_fsm.add_transition(TokenState.FLOAT, TokenState.SYMBOL, to_symbol)
_fsm.add_transition(TokenState.INT, TokenState.SYMBOL, int_to_symbol)
_fsm.add_transition(TokenState.NAME, TokenState.SYMBOL, to_symbol)
_fsm.add_transition(TokenState.STRING, TokenState.SYMBOL, to_symbol)

_fsm.add_transition(TokenState.SYMBOL, TokenState.COMMENT, symbol_to_comment)

_fsm.add_transition(TokenState.STRING, TokenState.ESCAPED, string_to_escaped)
_fsm.add_else_transition(TokenState.ESCAPED, TokenState.STRING)

_fsm.add_transition(TokenState.INT, TokenState.INT_DOT, int_to_int_dot)
_fsm.add_transition(TokenState.INT_DOT, TokenState.FLOAT, int_dot_to_float)
_fsm.add_transition(TokenState.INT_DOT, TokenState.NAME, int_dot_to_name)
_fsm.add_else_transition(TokenState.INT_DOT, TokenState.INT_DOT_ERROR)

def _step(tokens_and_state, char):
    (tokens, state) = tokens_and_state
    prev_state = _fsm.state
    (new_tokens, new_state) = _fsm.step((char, state))
    print(char + " + " + prev_state + " -> " + _fsm.state + " + " + str(map(lambda token: token.value, new_tokens)))
    return (tokens + new_tokens, new_state)

def tokenize(plaintext):
    (tokens, state) = reduce(_step, (plaintext + "\n"), ([], TokenizerState("", 1, 1, 1)))
    return tokens
