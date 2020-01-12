from tokenizer.tokenizer import tokenize
from syntax_parser.syntax_parser import build_abstract_syntax_tree, _rule_table, _build_rule_table, _derp 
from test.minimal_grammar import MinimalGrammar
from syntax_parser.rule_table import RuleTable

def _print_rule_column(column, indentation, indentation_size):
    print((" " * (indentation * indentation_size)) + "Token                Rule")
    for (token_type, result) in column.items():
        if type(result) == dict:
            print(
                (" " * (indentation * indentation_size)) +
                "+ " +
                token_type.name +
                " => ")
            _print_rule_column(result, indentation + 1, indentation_size)
        else:
            print(
                (" " * (indentation * indentation_size)) +
                "+ " +
                token_type.name +
                " => " +
                (" " * (15 - len(token_type.name))) +
                str(result))

def print_rule_table(rule_table, indentation=0, indentation_size=2):
    print((" " * (indentation * indentation_size)) + "Token         Stack              Rule")
    for (terminal_symbol, value) in rule_table.items():
        for (token_type, result) in value.items():
            if type(result) == dict:
                print(
                    (" " * (indentation * indentation_size)) +
                    token_type.name +
                    " + " +
                    (" " * (11 - len(token_type.name))) +
                    terminal_symbol.name +
                    " => ")
                _print_rule_column(result, indentation + 1, indentation_size)
            else:
                print(
                    (" " * (indentation * indentation_size)) +
                    token_type.name +
                    " + " +
                    (" " * (11 - len(token_type.name))) +
                    terminal_symbol.name +
                    " => " +
                    (" " * (15 - len(terminal_symbol.name))) +
                    str(result))


file_in = open("test/SimpleTest.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)
print("Number of tokens: " + str(len(tokens)))

_rule_table = _derp(MinimalGrammar)
print_rule_table(_rule_table)

#ast = build_abstract_syntax_tree(tokens, MinimalGrammar)
