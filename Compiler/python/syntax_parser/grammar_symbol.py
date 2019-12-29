from enum import Enum, EnumField
from token_type import TokenType

_SYMBOL_NAMES = [
    "FILE",
    "CODE",
    "MORE_CODE",
    "LINE",
    "TYPE",
    "INNER_TYPE",
    "CALL",
    "MORE_CALL",
    "FETCH",
    "R_FETCH",
    "VALUE"]


class GrammarSymbol:
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
    fundamental = Enum.value(GrammarSymbol, name)
    maybe = Enum.value(GrammarSymbol.Maybe, name)
    setattr(maybe, "inner", fundamental)
    GrammarSymbol.values.append(maybe)

for fundamental in vars(TokenType).values():
    if isinstance(fundamental, EnumField):
        base = Enum.value(GrammarSymbol.Base, fundamental.name, fundamental.value)
        setattr(base, "inner", fundamental)
        GrammarSymbol.values.append(base)

        maybe = Enum.value(GrammarSymbol.Maybe, fundamental.name, fundamental.value)
        setattr(maybe, "inner", fundamental)
        GrammarSymbol.values.append(maybe)

        maybe_base = Enum.value(GrammarSymbol.Maybe.Base, fundamental.name, fundamental.value)
        setattr(maybe_base, "inner", maybe)
        GrammarSymbol.values.append(maybe_base)
        GrammarSymbol.Maybe.values.append(maybe_base)
