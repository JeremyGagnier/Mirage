from mirage_enum import Enum, EnumField
from token_type import TokenType

_SYMBOL_NAMES = [
    "FILE",
    "CODE",
    "MORE_CODE",
    "LINE",
    "TYPE",
    "INNER_TYPE",
    "MORE_INNER_TYPE",
    "CALL",
    "MORE_CALL",
    "FETCH",
    "R_FETCH",
    "VALUE"]


class SimpleGrammarSymbol:
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
    fundamental = Enum.value(SimpleGrammarSymbol, name)
    maybe = Enum.value(SimpleGrammarSymbol.Maybe, name)
    setattr(maybe, "inner", fundamental)
    SimpleGrammarSymbol.values.append(maybe)

for fundamental in vars(TokenType).values():
    if isinstance(fundamental, EnumField):
        base = Enum.value(SimpleGrammarSymbol.Base, fundamental.name, fundamental.value)
        setattr(base, "inner", fundamental)
        SimpleGrammarSymbol.values.append(base)

        maybe = Enum.value(SimpleGrammarSymbol.Maybe, fundamental.name, fundamental.value)
        setattr(maybe, "inner", fundamental)
        SimpleGrammarSymbol.values.append(maybe)

        maybe_base = Enum.value(SimpleGrammarSymbol.Maybe.Base, fundamental.name, fundamental.value)
        setattr(maybe_base, "inner", base)
        SimpleGrammarSymbol.values.append(maybe_base)
        SimpleGrammarSymbol.Maybe.values.append(maybe_base)
