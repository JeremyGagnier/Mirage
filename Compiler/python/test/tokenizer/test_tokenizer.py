import tokenizer
from token_type import TokenType
from test_base import run_tests, verify_result

RESOURCES_PATH = "test/resources/"
MINIMAL_TEST_RESOURCE_NAME = "MinimalTest.mirage"
SIMPLE_TEST_RESOURCE_NAME = "SimpleTest.mirage"


def _get_resource(name):
    file_in = open(f"{RESOURCES_PATH}{name}", "r")
    resource_data = file_in.read()
    file_in.close()
    return resource_data


def tokenizer_should_classify_minimal_test():
    raw_text = _get_resource(MINIMAL_TEST_RESOURCE_NAME)

    expected_result = [
        TokenType.OBJECT,
        TokenType.NAME,
        TokenType.NEWLINE,
        TokenType.VAR,
        TokenType.NAME,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.INT]

    resulting_tokens = tokenizer.tokenize(raw_text)
    resulting_token_types = list(map(lambda token: token.token_type, resulting_tokens))

    verify_result(resulting_token_types, expected_result)


def tokenizer_should_classify_simple_test():
    raw_text = _get_resource(SIMPLE_TEST_RESOURCE_NAME)

    expected_result = [
        TokenType.OBJECT,
        TokenType.NAME,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.INT,
        TokenType.NEWLINE,
        TokenType.VAR,
        TokenType.NAME,
        TokenType.OPEN_TEMPLATE,
        TokenType.NAME,
        TokenType.CLOSE_TEMPLATE,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.NAME,
        TokenType.CLOSE_ARGUMENT,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.OPEN_TEMPLATE,
        TokenType.NAME,
        TokenType.CLOSE_TEMPLATE,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.NAME,
        TokenType.BIN_OP,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.NAME,
        TokenType.CLOSE_ARGUMENT,
        TokenType.BIN_OP,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.BIN_OP,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.INT,
        TokenType.COMMA,
        TokenType.INT,
        TokenType.CLOSE_ARGUMENT,
        TokenType.BIN_OP,
        TokenType.NEWLINE,
        TokenType.INT,
        TokenType.NEWLINE,
        TokenType.PUBLIC,
        TokenType.VAR,
        TokenType.NAME,
        TokenType.OPEN_TEMPLATE,
        TokenType.NAME,
        TokenType.COMMA,
        TokenType.NAME,
        TokenType.OPEN_TEMPLATE,
        TokenType.NAME,
        TokenType.CLOSE_TEMPLATE,
        TokenType.CLOSE_TEMPLATE,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.OPEN_ARGUMENT,
        TokenType.STRING,
        TokenType.COMMA,
        TokenType.NAME,
        TokenType.CLOSE_ARGUMENT,
        TokenType.COMMA,
        TokenType.OPEN_ARGUMENT,
        TokenType.STRING,
        TokenType.COMMA,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.INT,
        TokenType.COMMA,
        TokenType.INT,
        TokenType.COMMA,
        TokenType.INT,
        TokenType.CLOSE_ARGUMENT,
        TokenType.CLOSE_ARGUMENT,
        TokenType.CLOSE_ARGUMENT,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.OPEN_TEMPLATE,
        TokenType.NAME,
        TokenType.CLOSE_TEMPLATE,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.NAME,
        TokenType.DOT,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.STRING,
        TokenType.CLOSE_ARGUMENT,
        TokenType.NEWLINE,
        TokenType.NAME,
        TokenType.NAME,
        TokenType.EQUALS,
        TokenType.NAME,
        TokenType.COLON,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.CLOSE_ARGUMENT,
        TokenType.DOT,
        TokenType.NAME,
        TokenType.OPEN_ARGUMENT,
        TokenType.CLOSE_ARGUMENT]

    resulting_tokens = tokenizer.tokenize(raw_text)
    resulting_token_types = list(map(lambda token: token.token_type, resulting_tokens))

    verify_result(resulting_token_types, expected_result)


run_tests(
    tokenizer_should_classify_minimal_test,
    tokenizer_should_classify_simple_test)
