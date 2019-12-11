from grammar_symbol import GrammarSymbol
from rule_table import RuleTable


def _build_rule_table():
    return RuleTable([])


def _find_rule(stack_head, tokens, i, current_table):
    if i > len(tokens):
        raise Exception("Invalid syntax. Ran out of tokens when looking ahead.")

    table_or_rule = _rule_table[tokens[i]][stack_head]
    if isinstance(table_or_rule, RuleTable):
        _find_rule(stack_head, tokens, i + 1, table_or_rule)
    else:
        return table_or_rule


_rule_table = _build_rule_table()


def build_abstract_syntax_tree(tokens):
    i = 0
    stack = [GrammarSymbol.FILE]
    while i < len(tokens):
        next_token = tokens[i]
        stack_head = stack.pop()
        if next_token == stack_head:
            i += 1
        else:
            (a, new_symbols) = _find_rule(stack_head, tokens, i, _rule_table)
            stack += new_symbols[::-1]
