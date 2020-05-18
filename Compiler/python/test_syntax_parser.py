from tokenizer.tokenizer import tokenize
from syntax_parser.syntax_parser import build_abstract_syntax_tree, build_rule_table 
from test.minimal_grammar import MinimalGrammar
from test.minimal_grammar_symbol import MinimalGrammarSymbol
from syntax_parser.rule_table import RuleTable
from syntax_parser.ast import AST


def print_tokens(tokens):
    print("Tokens (" + str(len(tokens)) + "):")
    for token in tokens:
        print(str(token.token_type))


def print_rule_table(rule_table):
    def print_values(value, indentation=2, indentation_size=2):
        indentation_str = " " * (indentation * indentation_size)
        if type(value) == type({}):
            for (token_type, next_value) in value.items():
                print(indentation_str + str(token_type) + " =>")
                print_values(next_value, indentation + 1, indentation_size)
        else:
            print(indentation_str + str(value))

    print("Rule table:")
    for (terminal_symbol, value) in rule_table.items():
        print(str(terminal_symbol) + " =>")
        print_values(value)


def print_ast(ast):
    def print_rule(rule, indentation_str=""):
        (from_symbol, to_symbols) = rule.value
        to_symbols_str = str(list(map(lambda x: str(x), to_symbols)))
        print(indentation_str + str(from_symbol) + " -> " + to_symbols_str)

    def print_ast_helper(ast, indentation=1, indentation_size=2):
        indentation_str = " " * (indentation * indentation_size)
        for child in ast.children:
            if isinstance(child, AST):
                print_rule(child.rule, indentation_str)
                print_ast_helper(child, indentation + 1, indentation_size)
            elif child == None:
                print(indentation_str + "Nothing")
            else:
                print(indentation_str + str(child.token_type) + ": " + str(child.value))

    print("Abstract syntax tree:")
    print_rule(ast.rule)
    print_ast_helper(ast)


file_in = open("test/SimpleTest.mirage", "r")
tokenizer_text = file_in.read()
file_in.close()

tokens = tokenize(tokenizer_text)
print_tokens(tokens)
print()

rule_table = build_rule_table(MinimalGrammar, MinimalGrammarSymbol)
print_rule_table(rule_table)
print()

ast = build_abstract_syntax_tree(rule_table, tokens, MinimalGrammar, MinimalGrammarSymbol)
print_ast(ast)
