from tokenizer.tokenizer import tokenize

tokens = tokenize("""
test
123
123.456
(Int a) { a + 4 }
(1 + 3).toString()""")

print("Number of tokens: " + str(len(tokens)))
max_token_length = max(map(lambda token: len(token.value), tokens))
print("Type           Token" + (" " * (max_token_length - 4)) + "line:column")
for token in tokens:
    print(
        token.token_type +
        (" " * (15 - len(token.token_type))) +
        token.value +
        (" " * (max_token_length - len(token.value) + 1)) +
        str(token.line_num) +
        ":" +
        str(token.column_num))
