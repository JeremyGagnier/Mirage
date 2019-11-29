from grammar_parser import Grammar

with open("grammar.txt", "r") as grammar_file:
    Grammar(grammar_file.read())
