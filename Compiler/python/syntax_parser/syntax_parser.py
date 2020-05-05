from functools import reduce
from .ast import AST
from .grammar_symbol import GrammarSymbol
from .grammar import Grammar
from .rule_table import RuleTable

TERMINAL_SYMBOLS = filter(
    lambda x: x not in GrammarSymbol.Base.values and x not in GrammarSymbol.Maybe.values,
    GrammarSymbol.values)


def _get_possible_rules(grammar, terminal_symbol, lookahead, seen=[], requires_full_match=False):
    if terminal_symbol in seen:
        raise Exception(
            "Failed to build rule table from grammar. Terminal symbol " +
            terminal_symbol.name +
            " loops to itself: " +
            ", ".join(map(lambda x: str(x), seen)))

    possible_rules = []
    for rule in grammar.values:
        if rule.value == None:
            continue

        from_symbol, to_symbols = rule.value
        if from_symbol == terminal_symbol:
            print("  Calling rule matches lookahead for rule " + str(rule))
            matches_lookahead = _rule_matches_lookahead(grammar, to_symbols, lookahead, seen + [from_symbol])
            if requires_full_match:
                if matches_lookahead == True:
                    possible_rules.append(rule)
            elif matches_lookahead:
                possible_rules.append(rule)

    return possible_rules


def _rule_matches_lookahead(grammar, to_symbols, lookahead, seen):
    print("    Checking if " + str(list(map(lambda x: str(x), to_symbols))) + " matches " + str(list(map(lambda x: str(x), lookahead))))
    if len(lookahead) == 0:
        return True
    elif len(to_symbols) == 0:
        return lookahead
    elif lookahead[0] == to_symbols[0]:
        return _rule_matches_lookahead(grammar, to_symbols[1:], lookahead[1:], seen)
    elif to_symbols[0] not in GrammarSymbol.Base.values and to_symbols[0] not in GrammarSymbol.Maybe.values:
        print("  Getting possible rules from one symbol")
        possible_rules_from_one_symbol = _get_possible_rules(grammar, to_symbols[0], [lookahead[0]], seen, True)
        print("  Possible rules from one symbol: " + str(list(map(lambda x: str(x), possible_rules_from_one_symbol))))
        for rule in possible_rules_from_one_symbol:
            from_symbol, to_symbols2 = rule.value
            matches_lookahead = _rule_matches_lookahead(grammar, to_symbols2[1:], lookahead[1:], seen + [from_symbol])
            if type(matches_lookahead) is list:
                # Maybe need to recurse here, not thinking about it right now. Testing may reveal the answer.
                matches_lookahead2 = _rule_matches_lookahead(grammar, to_symbols[1:], matches_lookahead, seen)
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


def _derp(grammar=Grammar):
    rule_table = {}
    for terminal_symbol in TERMINAL_SYMBOLS:
        row = _build_rule_table(grammar, terminal_symbol, [])
        if len(row) != 0:
            rule_table[terminal_symbol] = row

    return rule_table

def _build_rule_table(grammar, terminal_symbol, lookahead):
    rule_table_row = {}
    for token_type in GrammarSymbol.Base.values:
        new_lookahead = lookahead + [token_type]

        print("Getting possible rules for stack " + str(terminal_symbol) + ", and seen tokens " + str(list(map(lambda x: str(x), new_lookahead))))
        valid_transitions = _get_possible_rules(grammar, terminal_symbol, new_lookahead)
        if len(valid_transitions) == 0:
            print("No valid transitions")
            pass
        elif len(valid_transitions) == 1:
            print("Exactly one valid transition")
            rule_table_row[token_type] = valid_transitions[0]
        else:
            print("More than one valid transition. Recursing: " + str(list(map(lambda x: str(x), valid_transitions))))
            rule_table_row[token_type] = _build_rule_table(grammar, terminal_symbol, new_lookahead)

    return rule_table_row


def _find_rule_starting_with(grammar, terminal_symbol, token_type, rules_searched=[]):
    def rules_filter(rule):
        return (rule.value[0] == terminal_symbol) and (rule not in rules_searched)

    filtered_rules = filter(rules_filter, grammar.values)
    for rule in filtered_rules:
        from_symbol, to_symbols = rule.value
        for to_symbol in to_symbols:
            if to_symbol in GrammarSymbol.Maybe.values:
                if to_symbol.inner in GrammarSymbol.Base:
                    if to_symbol.inner == token_type:
                        return True
                else:
                    if _find_rule_starting_with(grammar, to_symbol.inner, token_type, rules_searched + [rule]):
                        return True
            elif to_symbol in GrammarSymbol.Base.values:
                return (to_symbol == token_type)
            else:
                return _find_rule_starting_with(grammar, to_symbol, token_type, rules_searched + [rule])

    return False


def _build_rule_table2(grammar):
    rule_table = {}
    for terminal_symbol in TERMINAL_SYMBOLS:
        filtered_rules = filter(lambda rule: rule.value[0] == terminal_symbol, grammar.values)

        for token_type in GrammarSymbol.Base.values:
            valid_transitions = []

            for rule in filtered_rules:
                from_symbol, to_symbols = rule.value
                is_valid = False
                for to_symbol in to_symbols:
                    if to_symbol in GrammarSymbol.Maybe.values:
                        if to_symbol.inner in GrammarSymbol.Base:
                            if to_symbol.inner == token_type:
                                is_valid = True
                                break
                        else:
                            if _find_rule_starting_with(grammar, to_symbol.inner, token_type, rules_searched + [rule]):
                                is_valid = True
                                break
                    elif to_symbol in GrammarSymbol.Base.values:
                        is_valid = (to_symbol == token_type)
                        break
                    else:
                        is_valid = _find_rule_starting_with(grammar, to_symbol, token_type, rules_searched + [rule])
                        break

                if is_valid:
                    valid_transitions.append(rule)


            # If only one rule is valid set the rule, otherwise recurse
            if len(valid_transitions) == 1:
                rule_table[terminal_symbol] = {token_type: valid_transitions[0]}
            else:
                pass


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


_rule_table = {}#_build_rule_table()


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
