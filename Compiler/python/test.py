from tokenizer.tokenizer import tokenize

file_in = open("../Mirage/Tokenizer/Tokenizer.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)

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
