GRAMMAR_EXCEPTION_STRING = "Error parsing grammar - "
TOO_MANY_LONE_SYMBOLS = GRAMMAR_EXCEPTION_STRING + "Can only have one start symbol, all others lines must be terminals or rules. Offending symbol: '{0}'"
CAN_ONLY_DECLARE_ONCE = GRAMMAR_EXCEPTION_STRING + "Can only declare terminals once. Offending line: '{0}'"
DECLARATIONS_MUST_HAVE_MATCHES = GRAMMAR_EXCEPTION_STRING + "Terminal declarations must come with matches. Offending line: '{0}'"
UNRECOGNIZED_LINE_FORMAT = GRAMMAR_EXCEPTION_STRING + "Unrecogized line format. Offending line: '{0}'"
CYCLE_WITHOUT_INITIAL_TERMINAL_MSG = GRAMMAR_EXCEPTION_STRING + "There cannot be a rule cycle without generating at least one initial terminal symbol. Offending rule starts with '{0}'"
UNUSED_TERMINAL_MSG = GRAMMAR_EXCEPTION_STRING + "Terminal '{0}' is unused."
MISSING_RULE_MSG = GRAMMAR_EXCEPTION_STRING + "The symbol '{0}' is not terminal and has no associated rule."
NO_USAGE_OF_RULE_MSG = GRAMMAR_EXCEPTION_STRING + "Rules starting with symbol '{0}' aren't referenced and are thus unused."
START_SYMBOL_UNUSED_MSG = GRAMMAR_EXCEPTION_STRING + "The starting symbol '{0}' does not appear in any rules."

class Grammar:
    DEBUG = False

    def __init__(self, grammar_string):
        self.start = ""
        self.terminals = {}
        self.glyphs = {}
        self.rules = {}

        if Grammar.DEBUG:
            print("Parsing grammar:\n{0}...\n...{1}".format(grammar_string[:40], grammar_string[-40:]))

        for line in grammar_string.split('\n'):
            if line == "":
                continue

            parts = filter(lambda x: x != "", line.split("\\#")[0].split(" "))
            if len(parts) == 1:
                if self.start == "":
                    self.start = parts[0]
                else:
                    raise Exception(TOO_MANY_LONE_SYMBOLS.format(line))
            elif parts[1] == "<=":
                if parts[0] in self.terminals:
                    raise Exception(CAN_ONLY_DECLARE_ONCE.format(line))
                elif len(parts) <= 2:
                    raise Exception(DECLARATIONS_MUST_HAVE_MATCHES.format(line))
                self.terminals[parts[0]] = parts[2:]
                for glyph in parts[2:]:
                    self.glyphs[glyph] = parts[0]

            elif parts[1] == "=>":
                if parts[0] not in self.rules:
                    self.rules[parts[0]] = []
                self.rules[parts[0]].append(parts[2:])
            else:
                raise Exception(UNRECOGNIZED_LINE_FORMAT.format(line))

        found_symbols = set()
        found_terminals = set()
        def find_rule_with_terminal(symbol, seen):
            # Strip trailing question mark
            if symbol[-1] == '?':
                symbol = symbol[:-1]

            # Found a loop
            if symbol in seen:
                return False
            # Found a terminal, good!
            elif symbol in self.terminals:
                found_terminals.add(symbol)
                return True
            # Non-terminal. Check all rules.
            else:
                for results in self.rules[symbol]:
                    for s in results:
                        if s[-1] == '?':
                            s = s[:-1]
                        if s in self.terminals:
                            found_terminals.add(s)
                        else:
                            found_symbols.add(s)

                    for s in results:
                        if s[-1] == '?':
                            s = s[:-1]
                        found_symbols.add(s)

                    if not find_rule_with_terminal(results[0], list(seen) + [symbol]):
                        return False

                return True

        for rule_start in self.rules.keys():
            if not find_rule_with_terminal(rule_start, []):
                raise Exception(CYCLE_WITHOUT_INITIAL_TERMINAL_MSG.format(rule_start))

        for terminal in self.terminals.keys():
            if terminal not in found_terminals:
                raise Exception(UNUSED_TERMINAL_MSG.format(terminal))

        for symbol in found_symbols:
            if (symbol not in self.terminals) and (symbol not in self.rules):
                raise Exception(MISSING_RULE_MSG.format(symbol))

        for symbol in self.rules.keys():
            if symbol != self.start and symbol not in found_symbols:
                raise Exception(NO_USAGE_OF_RULE_MSG.format(symbol))

        if self.start not in self.rules:
            raise Exception(START_SYMBOL_UNUSED_MSG.format(symbol.start))

        if Grammar.DEBUG:
            print("Successfully parsed grammar")