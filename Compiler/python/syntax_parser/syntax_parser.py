from ast import AST
from grammar import Grammar
from grammar_symbol import GrammarSymbol
from rule_table import RuleTable
from functools import reduce

def _build_rule_table():
    return RuleTable({})


def _find_rule(stack_symbol, tokens, i, current_table):
    if i > len(tokens):
        raise Exception("Invalid syntax. Ran out of tokens when looking ahead.")
    
    current_token = tokens[i]
    if stack_symbol in GrammarSymbol.Maybe.values:
        stack_symbol = stack_symbol.inner 

    if current_token not in current_table.table or stack_symbol not in current_table.table[current_token]:
        return None

    table_or_rule = current_table.table[current_token][stack_symbol]
    if isinstance(table_or_rule, RuleTable):
        _find_rule(stack_symbol, tokens, i + 1, table_or_rule)
    else:
        return table_or_rule


_rule_table = _build_rule_table()


def _build_ast_helper(tokens, stack_symbol, token_index):
    if stack_symbol in GrammarSymbol.Base.values:
        if tokens[token_index].type == stack_symbol.inner:
            if token_index < len(tokens):
                return (token_index + 1, tokens[token_index])
            else:
                raise Exception("Invalid syntax. Expected more tokens.")
        else:
            raise Exception("Invalid syntax. Expected " + stack_symbol.name + " but got " + tokens[token_index].type.name)
    else:
        new_symbols = []
        rule = _find_rule(stack_symbol, tokens, token_index, _rule_table)
        if rule != None:
            (prev_symbol, new_symbols) = rule.value
        elif stack_symbol in GrammarSymbol.Maybe.values:
            rule = Grammar.MAYBE_TO_NOTHING
        else:
            raise Exception("Invalid syntax. Unexpected token.")

        def reduce_stack(i_and_ast_list, symbol):
            (i, ast_list) = i_and_ast_list
            (i_new, ast_new) = _build_ast_helper(tokens, symbol, i)
            return (i_new, ast_list + [ast_new])

        (i_new, ast_list) = reduce(reduce_stack, new_symbols, (token_index, []))
        return (i_new, AST(rule, ast_list))


def build_abstract_syntax_tree(tokens):
    (tokens_length, ast) = _build_ast_helper(tokens, GrammarSymbol.FILE, 0)
    return ast
