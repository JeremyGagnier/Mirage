from enum import Enum
from syntax_parser.grammar_symbol import GrammarSymbol


class MinimalGrammar:
    values = []

"""
Rule table should look like this (base symbol name to rule name):
{
	"OBJECT": "FILE",
	"VAR": "LINE_READONLY",
	"NAME": {
		"OPEN_TEMPLATE": "TEMPLATE_TYPE",
		"NAME": "TYPE",
		"COMMA": "TYPE"
	},
	"NEWLINE": "MORE_CODE",
	"COMMA": "MORE_INNER_TYPE"
}


SimpleTest.mirage should be parsed like this:

Tokens: OBJECT NAME NEWLINE VAR NAME EQUALS INT
Stack: FILE

FILE => OBJECT NAME NEWLINE CODE
CODE => LINE MORE_CODE?
LINE => VAR TYPE NAME EQUALS CALL
TYPE => NAME
CALL => VALUE
VALUE => INT
"""

Enum.value(MinimalGrammar, "MAYBE_TO_NOTHING")
Enum.value(MinimalGrammar, "FILE_OBJECT", (GrammarSymbol.FILE, [GrammarSymbol.Base.OBJECT, GrammarSymbol.Base.NAME, GrammarSymbol.Base.NEWLINE, GrammarSymbol.CODE]))

Enum.value(MinimalGrammar, "CODE", (GrammarSymbol.CODE, [GrammarSymbol.LINE, GrammarSymbol.Maybe.MORE_CODE]))
Enum.value(MinimalGrammar, "MORE_CODE", (GrammarSymbol.MORE_CODE, [GrammarSymbol.Base.NEWLINE, GrammarSymbol.CODE]))

Enum.value(MinimalGrammar, "LINE_READONLY", (GrammarSymbol.LINE, [GrammarSymbol.Maybe.Base.VAR, GrammarSymbol.TYPE, GrammarSymbol.Base.NAME, GrammarSymbol.Base.EQUALS, GrammarSymbol.CALL]))
#Enum.value(MinimalGrammar, "LINE_PUBLIC", (GrammarSymbol.LINE, [GrammarSymbol.Base.PUBLIC, GrammarSymbol.Maybe.Base.VAR, GrammarSymbol.TYPE, GrammarSymbol.Base.NAME, GrammarSymbol.Base.EQUALS, GrammarSymbol.CALL]))
#Enum.value(MinimalGrammar, "LINE_PRIVATE", (GrammarSymbol.LINE, [GrammarSymbol.Base.PRIVATE, GrammarSymbol.Maybe.Base.VAR, GrammarSymbol.TYPE, GrammarSymbol.Base.NAME, GrammarSymbol.Base.EQUALS, GrammarSymbol.CALL]))

Enum.value(MinimalGrammar, "TEMPLATE_TYPE", (GrammarSymbol.TYPE, [GrammarSymbol.Base.NAME, GrammarSymbol.Base.OPEN_TEMPLATE, GrammarSymbol.INNER_TYPE, GrammarSymbol.Base.CLOSE_TEMPLATE]))
Enum.value(MinimalGrammar, "TYPE", (GrammarSymbol.TYPE, [GrammarSymbol.Base.NAME]))
Enum.value(MinimalGrammar, "INNER_TYPE", (GrammarSymbol.INNER_TYPE, [GrammarSymbol.TYPE, GrammarSymbol.Maybe.MORE_INNER_TYPE]))
Enum.value(MinimalGrammar, "MORE_INNER_TYPE", (GrammarSymbol.MORE_INNER_TYPE, [GrammarSymbol.Base.COMMA, GrammarSymbol.INNER_TYPE]))

#Enum.value(MinimalGrammar, "CALL_BRACKETS", (GrammarSymbol.CALL, [GrammarSymbol.Base.OPEN_ARGUMENT, GrammarSymbol.CALL, GrammarSymbol.MORE_CALL, GrammarSymbol.Base.CLOSE_ARGUMENT, GrammarSymbol.MORE_CALL]))
#Enum.value(MinimalGrammar, "CALL_FETCH", (GrammarSymbol.CALL, [GrammarSymbol.FETCH, GrammarSymbol.MORE_CALL]))
#Enum.value(MinimalGrammar, "CALL_UNI_OP", (GrammarSymbol.CALL, [GrammarSymbol.Base.UNI_OP, GrammarSymbol.CALL]))
#Enum.value(MinimalGrammar, "CALL_VALUE", (GrammarSymbol.CALL, [GrammarSymbol.VALUE]))
#Enum.value(MinimalGrammar, "CALL_DOT", (GrammarSymbol.MORE_CALL, [GrammarSymbol.Base.DOT, GrammarSymbol.FETCH, GrammarSymbol.MORE_CALL]))
#Enum.value(MinimalGrammar, "CALL_BIN_OP", (GrammarSymbol.MORE_CALL, [GrammarSymbol.Base.BIN_OP, GrammarSymbol.CALL]))
#Enum.value(MinimalGrammar, "NO_MORE_CALL", (GrammarSymbol.MORE_CALL, []))

#Enum.value(MinimalGrammar, "FETCH_VALUE_DOT", (GrammarSymbol.FETCH, [GrammarSymbol.VALUE, GrammarSymbol.Base.DOT, GrammarSymbol.R_FETCH]))
#Enum.value(MinimalGrammar, "FETCH_NAME_DOT", (GrammarSymbol.FETCH, [GrammarSymbol.Base.NAME, GrammarSymbol.Base.DOT, GrammarSymbol.R_FETCH]))
#Enum.value(MinimalGrammar, "FETCH_NAME", (GrammarSymbol.FETCH, [GrammarSymbol.Base.NAME]))
#Enum.value(MinimalGrammar, "R_FETCH_DOT", (GrammarSymbol.R_FETCH, [GrammarSymbol.Base.NAME, GrammarSymbol.Base.DOT, GrammarSymbol.R_FETCH]))
#Enum.value(MinimalGrammar, "R_FETCH_NAME", (GrammarSymbol.R_FETCH, [GrammarSymbol.Base.NAME]))

#Enum.value(MinimalGrammar, "VALUE_FLOAT", (GrammarSymbol.VALUE, [GrammarSymbol.Base.FLOAT]))
#Enum.value(MinimalGrammar, "VALUE_INT", (GrammarSymbol.VALUE, [GrammarSymbol.Base.INT]))
#Enum.value(MinimalGrammar, "VALUE_STRING", (GrammarSymbol.VALUE, [GrammarSymbol.Base.STRING]))
