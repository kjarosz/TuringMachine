class TuringMachine:
    def __init__(self, desc_file):
        self.load_from_file(desc_file)
        self.reset()

    def load_from_file(self, input_machine):
        self.init_state = None
        self.final_states = None
        self.accepting_states = []
        self.transitions = {}
        with open(input_machine, "r") as i:
            for line in i:
                # Line comments
                if line.startswith("//"):
                    continue
                elif line.startswith("init_state:"):
                    self.init_state = line[len("init_state:"):].strip()
                elif line.startwith("final_states:"):
                    self.final_states = [x.strip() for x in line[len("final_states:"):].split(',')]
                elif line.startswith("["):
                    self.make_transition_function(line)

        if not self.init_state:
            raise Exception("Initial state is missing.")

        if not self.final_states:
            raise Exception("Final states are missing.")
                
    def make_transition_function(self, line):
        elements = [x.strip() for x in line.strip().strip('[]').split(',')]
        
        if not len(elements) == 4:
            raise Exception("Invalid transition function: {}".format(line))

        def check_function_operand(index):
            if len(elements[index]) > 0:
                return elements[index]
            raise Exception("Invalid operand.")

        state = get_function_operand(0)
        rsymbol = get_function_operand(1)
        wsymbol = get_function_operand(2)
        move = get_function_operand(3)

        if not (move == "<" or move == ">"):
            raise Exception("Invalid tape move {}.".format(move))

        if not state in self.transitions:
            self.transitions[state] = {}

        if rsymbol in self.transition[state]:
            raise Exception("Transition for ({}, {}) is defined more than once.".format(state, rsymbol))

        self.transition[state][rsymbol] = {
            "write": wsymbol,
            "move": self._move_left if "<" else self._move_right
        }

    def reset(self):
        self.current_state = self.init_state
        self.tape_position = 0
        self.tape = self.starting_tape
        self.halted = False

    def set_starting_tape(self, tape):
        self.starting_tape = tape

    def _move_left(self):
        self.tape_position = self.tape_position - 1

    def _move_right(self):
        self.tape_position = self.tape_position + 1

    def step(self):
        state = self.current_state
        symbol = self.tape[self.tape_position]

        if not self.current_state in self.transitions:
            self.halted = True

        if not self.tape[self.tape_position] in self.transitions[self.current_state]:
            self.halted = True

        transition = self.transition[state][symbol]

        self.tape[self.tape_position] = transitions["write"]
        self.transition["move"]()

    def run(self, print_machine_states=False):
        self.reset()
        while not self.halted:
            self.step()
            if print_machine_states:
                self.print_machine()
        print "Accepted" if self.current_state in self.final_states else "Rejected"
        self.print_machine()

    def print_machine(self):
        print "{} : [ {} ]".format(self.current_state, [('|{}|'.format(x) if i==self.tape_position else x) for i,x in enumerate(self.tape)])
