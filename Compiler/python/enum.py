class _EnumField:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name

class Enum:
    @staticmethod
    def value(obj, name, v = None):
        field = _EnumField(name, v)
        setattr(obj, name, field)
