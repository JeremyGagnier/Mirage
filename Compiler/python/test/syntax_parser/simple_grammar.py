from enum import Enum
from .simple_grammar_symbol import SimpleGrammarSymbol as G


class SimpleGrammar:
    values = []


Enum.value(SimpleGrammar, "FILE_OBJECT", 		(G.FILE, 			[G.Base.OBJECT, G.Base.NAME, G.Base.NEWLINE, G.CODE]))

Enum.value(SimpleGrammar, "CODE", 				(G.CODE, 			[G.LINE, G.Maybe.MORE_CODE]))
Enum.value(SimpleGrammar, "MORE_CODE", 			(G.MORE_CODE, 		[G.Base.NEWLINE, G.CODE]))

Enum.value(SimpleGrammar, "LINE_READONLY", 		(G.LINE, 			[G.Maybe.Base.VAR, G.TYPE, G.Base.NAME, G.Base.EQUALS, G.CALL]))
Enum.value(SimpleGrammar, "LINE_PUBLIC", 		(G.LINE, 			[G.Base.PUBLIC, G.Maybe.Base.VAR, G.TYPE, G.Base.NAME, G.Base.EQUALS, G.CALL]))
Enum.value(SimpleGrammar, "LINE_PRIVATE", 		(G.LINE, 			[G.Base.PRIVATE, G.Maybe.Base.VAR, G.TYPE, G.Base.NAME, G.Base.EQUALS, G.CALL]))

Enum.value(SimpleGrammar, "TEMPLATE_TYPE", 		(G.TYPE,			[G.Base.NAME, G.Base.OPEN_TEMPLATE, G.INNER_TYPE, G.Base.CLOSE_TEMPLATE]))
Enum.value(SimpleGrammar, "TYPE", 				(G.TYPE, 			[G.Base.NAME]))
Enum.value(SimpleGrammar, "INNER_TYPE", 		(G.INNER_TYPE, 		[G.TYPE, G.Maybe.MORE_INNER_TYPE]))
Enum.value(SimpleGrammar, "MORE_INNER_TYPE", 	(G.MORE_INNER_TYPE, [G.Base.COMMA, G.INNER_TYPE]))

Enum.value(SimpleGrammar, "CALL_BRACKETS", 		(G.CALL, 			[G.Base.OPEN_ARGUMENT, G.CALL, G.MORE_CALL, G.Base.CLOSE_ARGUMENT, G.MORE_CALL]))
Enum.value(SimpleGrammar, "CALL_FETCH", 		(G.CALL, 			[G.FETCH, G.MORE_CALL]))
Enum.value(SimpleGrammar, "CALL_UNI_OP", 		(G.CALL, 			[G.Base.UNI_OP, G.CALL]))
Enum.value(SimpleGrammar, "CALL_VALUE", 		(G.CALL, 			[G.VALUE]))
Enum.value(SimpleGrammar, "CALL_DOT", 			(G.MORE_CALL, 		[G.Base.DOT, G.FETCH, G.MORE_CALL]))
Enum.value(SimpleGrammar, "CALL_BIN_OP", 		(G.MORE_CALL, 		[G.Base.BIN_OP, G.CALL]))
Enum.value(SimpleGrammar, "NO_MORE_CALL", 		(G.MORE_CALL, 		[]))

Enum.value(SimpleGrammar, "FETCH_VALUE_DOT", 	(G.FETCH, 			[G.VALUE, G.Base.DOT, G.R_FETCH]))
Enum.value(SimpleGrammar, "FETCH_NAME_DOT", 	(G.FETCH, 			[G.Base.NAME, G.Base.DOT, G.R_FETCH]))
Enum.value(SimpleGrammar, "FETCH_NAME", 		(G.FETCH, 			[G.Base.NAME]))
Enum.value(SimpleGrammar, "R_FETCH_DOT", 		(G.R_FETCH, 		[G.Base.NAME, G.Base.DOT, G.R_FETCH]))
Enum.value(SimpleGrammar, "R_FETCH_NAME", 		(G.R_FETCH, 		[G.Base.NAME]))

Enum.value(SimpleGrammar, "VALUE_FLOAT", 		(G.VALUE, 			[G.Base.FLOAT]))
Enum.value(SimpleGrammar, "VALUE_INT", 			(G.VALUE, 			[G.Base.INT]))
Enum.value(SimpleGrammar, "VALUE_STRING", 		(G.VALUE, 			[G.Base.STRING]))
