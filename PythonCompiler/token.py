class Token():
    def __init__(self, token_type, value, line_num, column_num):
        self.token_type = token_type
        self.value = value
        self.line_num = line_num
        self.column_num = column_num
        