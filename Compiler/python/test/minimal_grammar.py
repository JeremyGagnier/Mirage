from enum import Enum
from .minimal_grammar_symbol import MinimalGrammarSymbol as G


class MinimalGrammar:
    values = []


Enum.value(MinimalGrammar, "FILE_OBJECT", 	(G.FILE, 		[G.Base.OBJECT, G.Base.NAME, G.Base.NEWLINE, G.CODE]))
Enum.value(MinimalGrammar, "CODE", 			(G.CODE, 		[G.LINE, G.Maybe.MORE_CODE]))
Enum.value(MinimalGrammar, "MORE_CODE", 	(G.MORE_CODE, 	[G.Base.NEWLINE, G.CODE]))
Enum.value(MinimalGrammar, "LINE_READONLY", (G.LINE, 		[G.Maybe.Base.VAR, G.TYPE, G.Base.NAME, G.Base.EQUALS, G.CALL]))
Enum.value(MinimalGrammar, "TYPE", 			(G.TYPE, 		[G.Base.NAME]))
Enum.value(MinimalGrammar, "CALL_VALUE", 	(G.CALL, 		[G.VALUE]))
Enum.value(MinimalGrammar, "VALUE_INT", 	(G.VALUE, 		[G.Base.INT]))
