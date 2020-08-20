class TokenizerException(Exception):
    def __init__(self, exception_type, line_num, column_num, offender):
        self.exception_type = exception_type
        self.line_num = line_num
        self.column_num = column_num
        self.offender = offender

    def __str__(self):
        return self.exception_type.value.format(self.line_num, self.column_num, self.offender)
