from tokenizer.tokenizer import tokenize
from syntax_parser.syntax_parser import build_abstract_syntax_tree, _rule_table, _build_rule_table
from test.minimal_grammar import MinimalGrammar

file_in = open("test/SimpleTest.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)
print("Number of tokens: " + str(len(tokens)))

_rule_table = _build_rule_table(MinimalGrammar)

#ast = build_abstract_syntax_tree(tokens, MinimalGrammar)
