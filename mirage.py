import sys
from tokenizer import Tokenizer
from syntax_parser import Syntax
from grammar_parser import Grammar

with open("grammar.txt", "r") as grammar_file:
    grammar_str = grammar_file.read()
with open(sys.argv[1]) as code_file:
    code_str = code_file.read()

grammar = Grammar(grammar_str)
tokenizer = Tokenizer(grammar, code_str)
syntax = Syntax(grammar, tokenizer)
print("Compiled")
