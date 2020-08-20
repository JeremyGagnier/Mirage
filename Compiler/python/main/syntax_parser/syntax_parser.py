from functools import reduce
from ast import AST
from grammar_symbol import GrammarSymbol
from grammar import Grammar
from rule_table import RuleTable


def _is_stack_in_symbols(grammar, grammar_symbol, symbols, stack, rules_searched = []):
    if stack[0] == grammar_symbol.Base.VAR:
        should_print = True
    while len(symbols) > 0 and len(stack) > 0:

        if symbols[0] in grammar_symbol.Maybe.values:
            is_maybe = True
            actual_symbol = symbols[0].inner
        else:
            is_maybe = False
            actual_symbol = symbols[0]

        if actual_symbol in grammar_symbol.Base.values:
            if actual_symbol == stack[0]:
                symbols = symbols[1:]
                stack = stack[1:]
            elif is_maybe:
                symbols = symbols[1:]
            else:
                return None
        else:
            def rules_filter(rule):
                return (rule.value[0] == actual_symbol) and (rule not in rules_searched)

            filtered_rules = filter(rules_filter, grammar.values)

            for rule in filtered_rules:
                from_symbol, to_symbols = rule.value
                # This assumes that the first successful rule is the correct one, but some successful rules will
                # fail to exhaust the stack later. The exact rule that successfully exhausts the stack should be
                # searched for instead, but that may be exponential time complexity.
                stack_opt = _is_stack_in_symbols(grammar, grammar_symbol, to_symbols, stack, rules_searched + [rule])
                if (stack_opt != None):
                    stack = stack_opt
                    symbols = symbols[1:]
                    break
            else:
                if is_maybe:
                    symbols = symbols[1:]
                else:
                    return None

    return stack


def _get_valid_transitions(grammar, grammar_symbol, terminal_symbol, stack):
    filtered_rules = filter(lambda rule: rule.value[0] == terminal_symbol, grammar.values)
    valid_transitions = []
    for rule in filtered_rules:
        from_symbol, to_symbols = rule.value
        if _is_stack_in_symbols(grammar, grammar_symbol, to_symbols, stack) == []:
            valid_transitions.append(rule)

    return valid_transitions


def _build_rule_table_helper(grammar, grammar_symbol, terminal_symbol, stack):
    result = {}
    for token_type in grammar_symbol.Base.values:
        valid_transitions = _get_valid_transitions(grammar, grammar_symbol, terminal_symbol, stack + [token_type])
        if len(valid_transitions) == 1:
            result[token_type.inner] = valid_transitions[0]
        elif len(valid_transitions) > 1:
            result[token_type.inner] = _build_rule_table_helper(grammar, grammar_symbol, terminal_symbol, stack + [token_type])

    return result


def _find_rule(rule_table, grammar, stack_symbol, tokens, token_index, is_maybe):
    if stack_symbol not in rule_table:
        if is_maybe:
            return None
        else:
            raise Exception("Invalid grammar. " + stack_symbol.name + " has no transitions.")
    else:
        lookahead = rule_table[stack_symbol]
        while (token_index < len(tokens)) and (tokens[token_index].token_type in lookahead):
            lookahead = lookahead[tokens[token_index].token_type]
            if type(lookahead) != type({}):
                return lookahead
            token_index += 1

        if is_maybe:
            return None
        elif token_index >= len(tokens):
            raise Exception("Invalid syntax. Expected more tokens.")
        else:
            raise Exception("Invalid syntax. Found unexpected token " + tokens[token_index].token_type.name)


def _build_ast_helper(rule_table, grammar, grammar_symbol, tokens, stack_symbol, token_index):
    if stack_symbol in grammar_symbol.Maybe.values:
        is_maybe = True
        actual_symbol = stack_symbol.inner
    else:
        is_maybe = False
        actual_symbol = stack_symbol

    if actual_symbol in grammar_symbol.Base.values:
        if tokens[token_index].token_type == actual_symbol.inner:
            if token_index < len(tokens):
                return (token_index + 1, tokens[token_index])
            elif is_maybe:
                return (token_index, None)
            else:
                raise Exception("Invalid syntax. Expected more tokens.")
        elif is_maybe:
            return (token_index, None)
        else:
            raise Exception("Invalid syntax. Expected " + actual_symbol.name + " but got " + tokens[token_index].token_type.name)
    else:
        rule = _find_rule(rule_table, grammar, actual_symbol, tokens, token_index, is_maybe)
        if rule == None:
            return (token_index, None)
        else:
            (prev_symbol, new_symbols) = rule.value

            def reduce_stack(i_and_ast_list, symbol):
                (i, ast_list) = i_and_ast_list
                (i_new, ast_new) = _build_ast_helper(rule_table, grammar, grammar_symbol, tokens, symbol, i)
                return (i_new, ast_list + [ast_new])

            (i_new, ast_list) = reduce(reduce_stack, new_symbols, (token_index, []))
            return (i_new, AST(rule, ast_list))


def build_abstract_syntax_tree(rule_table, tokens, grammar=Grammar, grammar_symbol=GrammarSymbol):
    (tokens_length, ast) = _build_ast_helper(rule_table, grammar, grammar_symbol, tokens, grammar_symbol.FILE, 0)
    return ast


def build_rule_table(grammar=Grammar, grammar_symbol=GrammarSymbol):
    def terminal_symbols_filter(symbol):
        return (symbol not in grammar_symbol.Base.values) and (symbol not in grammar_symbol.Maybe.values)

    terminal_symbols = filter(terminal_symbols_filter, grammar_symbol.values)

    rule_table = {}
    for terminal_symbol in terminal_symbols:
        rule_table[terminal_symbol] = _build_rule_table_helper(grammar, grammar_symbol, terminal_symbol, [])

    return rule_table
