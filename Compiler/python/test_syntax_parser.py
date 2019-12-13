from tokenizer.tokenizer import tokenize
from syntax_parser.syntax_parser import build_abstract_syntax_tree

file_in = open("../Mirage/Tokenizer/Tokenizer.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)
print("Number of tokens: " + str(len(tokens)))

ast = build_abstract_syntax_tree(tokens)
