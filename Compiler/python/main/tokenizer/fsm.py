class FSM():
    def __init__(self, initial_state):
        self.state = initial_state
        self.states = {}
        self.transitions = {}
        self.else_transitions = {}

    def add_state(self, state, action):
        if state in self.states:
            raise Exception("Tried to add existing state to FSM")
        self.states[state] = action

    def add_transition(self, from_state, to_state, predicate):
        if from_state not in self.transitions:
            self.transitions[from_state] = [(to_state, predicate)]
        else:
            for (state, p) in self.transitions[from_state]:
                if state == to_state:
                    raise Exception("Tried to add duplicate transition to FSM")
            self.transitions[from_state].append((to_state, predicate))

    def add_else_transition(self, from_state, to_state):
        if from_state in self.else_transitions:
            raise Exception("Tried to add multiple else transitions to the same state")
        self.else_transitions[from_state] = to_state

    def step(self, data):
        previous_state = self.state
        transitioned = False
        if self.state in self.transitions:
            for (state, predicate) in self.transitions[self.state]:
                if predicate(data):
                    transitioned = True
                    self.state = state
                    break

        if not transitioned and self.state in self.else_transitions:
            self.state = self.else_transitions[self.state]

        return self.states[self.state](previous_state, data)
