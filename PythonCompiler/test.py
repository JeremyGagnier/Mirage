from Tokenizer.tokenizer import tokenize

tokens = tokenize("""
test
123
123.456
(Int a) { a + 4 }""")

#print("Number of tokens: " + str(len(tokens)))
max_token_length = max(map(lambda token: len(token.value), tokens))
#print("Type           Token" + (" " * (max_token_length - 4)) + "line:column")
for token in tokens:
    pass
    """print(
        token.token_type +
        (" " * (15 - len(token.token_type))) +
        token.value +
        (" " * (max_token_length - len(token.value) + 1)) +
        str(token.line_num) +
        ":" +
        str(token.column_num))"""
