from enum import Enum
from syntax_parser.grammar_symbol import GrammarSymbol

class MinimalGrammar:
    values = []


Enum.value(SimpleGrammar, "MAYBE_TO_NOTHING")
Enum.value(SimpleGrammar, "FILE", (GrammarSymbol.FILE, [GrammarSymbol.Base.OBJECT, GrammarSymbol.Base.NAME, GrammarSymbol.CODE]))

Enum.value(SimpleGrammar, "CODE", (GrammarSymbol.CODE, [GrammarSymbol.LINE, GrammarSymbol.Maybe.MORE_CODE]))
Enum.value(SimpleGrammar, "MORE_CODE", (GrammarSymbol.MORE_CODE, [GrammarSymbol.Base.NEWLINE, GrammarSymbol.CODE]))

Enum.value(SimpleGrammar, "FILE", (GrammarSymbol.FILE, [GrammarSymbol.Base.OBJECT, GrammarSymbol.Base.NAME, GrammarSymbol.CODE]))
Enum.value(SimpleGrammar, "FILE", (GrammarSymbol.FILE, [GrammarSymbol.Base.OBJECT, GrammarSymbol.Base.NAME, GrammarSymbol.CODE]))
Enum.value(SimpleGrammar, "FILE", (GrammarSymbol.FILE, [GrammarSymbol.Base.OBJECT, GrammarSymbol.Base.NAME, GrammarSymbol.CODE]))
"""
FILE => OBJECT NAME CODE

CODE => LINE MORE_CODE?
MORE_CODE => NEWLINE CODE

LINE => VAR? TYPE NAME EQUALS CALL
LINE => PUBLIC TYPE NAME EQUALS CALL
LINE => PRIVATE TYPE NAME EQUALS CALL

TYPE => NAME OPEN_TEMPLATE INNER_TYPE CLOSE_TEMPLATE
TYPE => NAME
INNER_TYPE => TYPE COMMA INNER_TYPE
INNER_TYPE => TYPE

CALL => OPEN_ARGUMENT CALL MORE_CALL? CLOSE_ARGUMENT MORE_CALL?
CALL => FETCH MORE_CALL?
CALL => UNI_OP CALL
CALL => VALUE
MORE_CALL => DOT FETCH MORE_CALL?
MORE_CALL => BIN_OP CALL

FETCH => VALUE DOT R_FETCH
FETCH => NAME DOT R_FETCH
FETCH => NAME
R_FETCH => NAME DOT R_FETCH
R_FETCH => NAME

VALUE => FLOAT
VALUE => INT
VALUE => STRING
"""