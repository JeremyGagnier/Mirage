from enum import Enum, EnumField
from token_type import TokenType

_SYMBOL_NAMES = [
    "FILE",
    "CODE",
    "MORE_CODE",
    "LINE",
    "TYPE",
    "CALL",
    "VALUE"]


class MinimalGrammarSymbol:
    values = []


    class Base:
        values = []


    class Maybe:
        values = []


        class Base:
            values = []


# Fills in the classes with downwards references and adds to the value lists. This setup allows checking whether or not
# an inner enum type contains a field and other useful things.
for name in _SYMBOL_NAMES:
    fundamental = Enum.value(MinimalGrammarSymbol, name)
    maybe = Enum.value(MinimalGrammarSymbol.Maybe, name)
    setattr(maybe, "inner", fundamental)
    MinimalGrammarSymbol.values.append(maybe)

for fundamental in vars(TokenType).values():
    if isinstance(fundamental, EnumField):
        base = Enum.value(MinimalGrammarSymbol.Base, fundamental.name, fundamental.value)
        setattr(base, "inner", fundamental)
        MinimalGrammarSymbol.values.append(base)

        maybe = Enum.value(MinimalGrammarSymbol.Maybe, fundamental.name, fundamental.value)
        setattr(maybe, "inner", fundamental)
        MinimalGrammarSymbol.values.append(maybe)

        maybe_base = Enum.value(MinimalGrammarSymbol.Maybe.Base, fundamental.name, fundamental.value)
        setattr(maybe_base, "inner", maybe)
        MinimalGrammarSymbol.values.append(maybe_base)
        MinimalGrammarSymbol.Maybe.values.append(maybe_base)
