class TokenizerState():
    def __init__(self, token_text, token_start_column, line_num, column_num, parentheses_depth=0, was_newline=False):
        self.token_text = token_text
        self.token_start_column = token_start_column
        self.line_num = line_num
        self.column_num = column_num
        self.parentheses_depth = parentheses_depth
        self.was_newline = was_newline
