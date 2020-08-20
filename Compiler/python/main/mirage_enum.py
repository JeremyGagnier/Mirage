_FIELD_COUNTER = 0
class EnumField:
    def __init__(self, name, value):
        global _FIELD_COUNTER
        self._id = _FIELD_COUNTER
        _FIELD_COUNTER += 1

        self.name = name
        self.value = value


    def __str__(self):
        return self.name


class Enum:
    @staticmethod
    def value(obj, name, v = None):
        field = EnumField(name, v)
        obj.values.append(field)
        setattr(obj, name, field)
        return field
