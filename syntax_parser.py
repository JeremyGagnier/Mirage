SYNTAX_EXCEPTION_STRING = "Error parsing syntax - "
UNEXPECTED_NEWLINE_MSG = SYNTAX_EXCEPTION_STRING + "Unexpected newline at line {0}, likely due to a compiler bug."
BAD_SYNTAX_MSG = SYNTAX_EXCEPTION_STRING + "Bad syntax at line {0}, on symbol '{1}'"

class Node():
    def __init__(self, symbol, parent, children):
        self.symbol = symbol
        self.parent = parent
        self.children = children


class Stack():
    def __init__(self, symbol_stack):
        self.stack = symbol_stack
        self.rule_order = []
        self.index = 0


    def pop(self):
        return self.stack.pop()


    def copy_and_add(self, symbols, rule_symbol, rule_index):
        s = Stack(list(self.stack))
        s.rule_order = list(self.rule_order)
        s.index = self.index

        for i in range(len(symbols), 0, -1):
            s.stack.append(symbols[i - 1])
        s.rule_order.append((rule_symbol, rule_index))

        return s


    def increment(self):
        self.index += 1
        return self

class Syntax:
    DEBUG = False

    def __init__(self, grammar, tokenizer):
        # This algorithm uses a nondeterministic pushdown automaton
        # List[Token] -> List[Tuple[string, int]]
        # In : A list of code tokens to parse
        # Out: A list of rules in order of their usage
        if Syntax.DEBUG:
            print("Parsing tokens: " + str(tokenizer.tokens))

        stacks = [Stack([grammar.start])]

        deepest_index = 0
        next_stacks = []
        self.rule_order = None
        while True:
            for stack in stacks:
                #if stack.index >= len(tokenizer.tokens):
                #    self.rule_order = stack.rule_order
                #    break

                if stack.index > deepest_index:
                    deepest_index = stack.index

                input_symbol = tokenizer.tokens[stack.index].name

                optional = False
                stack_symbol = stack.pop()
                if stack_symbol[-1] == "?":
                    optional = True
                    stack_symbol = stack_symbol[:-1]

                if stack_symbol != input_symbol:
                    if optional:
                        if len(stack.stack) > 0:
                            next_stacks.append(stack)
                    if stack_symbol not in grammar.rules:
                        continue
                    rule_list = grammar.rules[stack_symbol]
                    for r in range(len(rule_list)):
                        next_stacks.append(stack.copy_and_add(rule_list[r], stack_symbol, r))

                elif len(stack.stack) > 0:
                    next_stacks.append(stack.increment())

                elif stack.index + 1 >= len(tokenizer.tokens):
                    self.rule_order = stack.rule_order
                    break

            if self.rule_order != None:
                break

            if next_stacks == []:
                bad_line = tokenizer.tokens[deepest_index].line_num
                bad_symbol = tokenizer.tokens[deepest_index].token_str
                if bad_symbol == "\n":
                    print(UNEXPECTED_NEWLINE_MSG.format(bad_line + 2))
                else:
                    print(BAD_SYNTAX_MSG.format(bad_line + 1, bad_symbol))
                return None

            if Syntax.DEBUG:
                #if (deepest_index > 400):
                    print("\nSTACK:")
                    for stack in next_stacks:
                        token_stack_end = stack.index + min(10, len(tokenizer.tokens) - stack.index)
                        parser_stack_end = min(10, len(stack.stack))
                        print(str(stack.index) + ", " +
                            str([x.name for x in tokenizer.tokens[stack.index:token_stack_end]]) + ", " +
                            str(stack.stack[::-1][:parser_stack_end]))

            stacks = next_stacks
            next_stacks = []

        if Syntax.DEBUG:
            print("Finished parsing syntax. {0} rule applications.".format(len(self.rule_order)))
