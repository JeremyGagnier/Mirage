from enum import Enum
from syntax_parser.grammar_symbol import GrammarSymbol


class SimpleGrammar:
    values = []


# TODO: Finish simple grammar
Enum.value(SimpleGrammar, "MAYBE_TO_NOTHING")
Enum.value(SimpleGrammar, "FILE", (GrammarSymbol.FILE, [GrammarSymbol.Maybe.IMPORT_DECLS, GrammarSymbol.TEST_OR_ENUM_OR_OBJECT]))
Enum.value(SimpleGrammar, "TEST_OR_ENUM_OR_OBJECT", (GrammarSymbol.TEST_OR_ENUM_OR_OBJECT, [GrammarSymbol.Maybe.OBJECT_DEFINITION, GrammarSymbol.Maybe.CLASS_DEFINITION]))
