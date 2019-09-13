class TransitionData:
    def __init__(self, from_state, to_state, symbol, peek_value, push_value):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol
        self.peek_value = peek_value
        self.push_value = push_value

class Node:
    def __init__(self, name, transitions=[]):
        self.name = name
        self.transitions = {}
        self.epsilon = None
        for transition in transitions:
            if transition.symbol == None:
                if self.epsilon != None:
                    self.epsilon.append(transition)
                else:
                    self.epsilon = [transition]

            elif transition.symbol in self.transitions:
                self.transitions[symbol].append(transition)
            else:
                self.transitions[symbol] = [transition]


class PDA:
    def __init__(self, transitions_string):
        transitions = {}
        lines = transitions_string.split("\n")
        for line in lines:
            data, comment = line.split("#")

            words = []
            word = ""
            for char in data:
                if char == " " && word != "":
                    words.append(word)
                    word = ""
                else:
                    word += char
            if word != "":
                words.append(word)

            from_state, to_state, symbol, peek_value, push_value = words
            if symbol == "0":
                symbol = None
            if peek_value == "0":
                peek_value = None
            if push_value == "0":
                push_value = None
            transition = TransitionData(from_state, to_state, symbol, peek_value, push_value)
            if from_state in transitions:
                transitions[from_state].append(transition)
            else:
                transitions[from_state] = [transition]

        self.nodes = {}
        for node_name in transitions.keys():
            nodes[node_name] = Node(node_name, transitions[node_name])



