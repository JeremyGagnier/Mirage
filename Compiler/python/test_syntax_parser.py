from tokenizer.tokenizer import tokenize
from syntax_parser.syntax_parser import build_abstract_syntax_tree, build_rule_table 
from test.minimal_grammar import MinimalGrammar
from test.minimal_grammar_symbol import MinimalGrammarSymbol
from syntax_parser.rule_table import RuleTable


def _print_values(value, indentation=2, indentation_size=2):
    indentation_str = " " * (indentation * indentation_size)
    if type(value) == type({}):
        for (token_type, next_value) in value.items():
            print(indentation_str + str(token_type) + " =>")
            _print_values(next_value, indentation + indentation_size, indentation_size)
    else:
        print(indentation_str + str(value))


def print_rule_table(rule_table):
    for (terminal_symbol, value) in rule_table.items():
        print(str(terminal_symbol) + " =>")
        _print_values(value)


file_in = open("test/SimpleTest.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)
print("Number of tokens: " + str(len(tokens)))

rule_table = build_rule_table(MinimalGrammar, MinimalGrammarSymbol)
print_rule_table(rule_table)

ast = build_abstract_syntax_tree(rule_table, tokens, MinimalGrammar, MinimalGrammarSymbol)
