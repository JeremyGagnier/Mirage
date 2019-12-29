from ast import AST
from grammar_symbol import GrammarSymbol
from grammar import Grammar
from rule_table import RuleTable
from functools import reduce

TRANSITIONAL_SYMBOLS = filter(
    lambda x: x not in GrammarSymbol.Base.values and x not in GrammarSymbol.Maybe.values,
    GrammarSymbol.values)


def _get_possible_rules(grammar, transitional_symbol, lookahead, seen=[]):
    if transitional_symbol in seen:
        raise Exception(
            "Failed to build rule table from grammar. Transitional symbol " +
            transitional_symbol.name +
            " loops to itself.")

    possible_rules = []
    for rule in grammar.values:
        from_symbol, to_symbols = rule.value
        if from_symbol == transitional_symbol and _rule_matches_lookahead(grammar, to_symbols, [lookahead], seen + [rule]):
            possible_rules.append(rule)

    return possible_rules


def _rule_matches_lookahead(grammar, to_symbols, lookahead, seen):
    if len(lookahead) == 0:
        return True
    elif len(to_symbols) == 0:
        return lookahead
    elif lookahead[0] == to_symbols[0]:
        return _rule_matches_lookahead(grammar, to_symbols[1:], lookahead[1:], seen)
    elif to_symbols[0] not in GrammarSymbol.Base.values and to_symbols[0] not in GrammarSymbol.Maybe.values:
        possible_rules_from_one_symbol = _get_possible_rules(grammar, to_symbols[0], [lookahead[0]], seen)
        for rule in possible_rules_from_one_symbol:
            from_symbol, to_symbols2 = rule.value
            matches_lookahead = _rule_matches_lookahead(grammar, to_symbols2[1:], lookahead[1:], seen + [rule])
            if type(matches_lookahead) is list:
                # Maybe need to recurse here, not thinking about it right now. Testing may reveal the answer.
                matches_lookahead2 = _rule_matches_lookahead(grammar, to_symbol[1:], matches_lookahead, seen)
                if matches_lookahead2 == True:
                    return True
            elif matches_lookahead == True:
                return True
        else:
            return False
    elif to_symbols[0] in GrammarSymbol.Maybe.values:
        matches_lookahead = _rule_matches_lookahead(grammar, [to_symbols[0].inner] + to_symbols[1:], lookahead, seen)
        if type(matches_lookahead) is list or not matches_lookahead:
            return _rule_matches_lookahead(grammar, to_symbols[1:], lookahead, seen)
        else:
            return True
    else:
        return False


def _build_rule_table(grammar=Grammar, lookahead=[]):
    rule_table = {}
    for token_type in GrammarSymbol.Base.values:
        rule_table_row = {}
        new_lookahead = lookahead + [token_type]
        for transitional_symbol in TRANSITIONAL_SYMBOLS:
            valid_transitions = _get_possible_rules(grammar, transitional_symbol, new_lookahead)
            if len(valid_transitions) == 0:
                pass
            elif len(valid_transitions) == 1:
                rule_table_row[transitional_symbol] = valid_transitions[0]
            else:
                rule_table_row[transitional_symbol] = _build_rule_table(grammar, new_lookahead)

        if len(rule_table_row) != 0:
            rule_table[token_type] = rule_table_row


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


def _build_ast_helper(grammar, tokens, stack_symbol, token_index):
    if stack_symbol in GrammarSymbol.Base.values:
        if tokens[token_index].type == stack_symbol.inner:
            if token_index < len(tokens):
                return (token_index + 1, tokens[token_index])
            else:
                raise Exception("Invalid syntax. Expected more tokens.")
        else:
            raise Exception(
                "Invalid syntax. Expected " + stack_symbol.name + " but got " + tokens[token_index].type.name)
    else:
        new_symbols = []
        rule = _find_rule(stack_symbol, tokens, token_index, _rule_table)
        if rule != None:
            (prev_symbol, new_symbols) = rule.value
        elif stack_symbol in GrammarSymbol.Maybe.values:
            rule = grammar.MAYBE_TO_NOTHING
        else:
            raise Exception("Invalid syntax. Unexpected token.")

        def reduce_stack(i_and_ast_list, symbol):
            (i, ast_list) = i_and_ast_list
            (i_new, ast_new) = _build_ast_helper(tokens, symbol, i)
            return (i_new, ast_list + [ast_new])

        (i_new, ast_list) = reduce(reduce_stack, new_symbols, (token_index, []))
        return (i_new, AST(rule, ast_list))


def build_abstract_syntax_tree(tokens, grammar=Grammar):
    (tokens_length, ast) = _build_ast_helper(grammar, tokens, GrammarSymbol.FILE, 0)
    return ast
