#
# Description:
#
# Main class representing a Turing Machine loaded from a description file. 
# There is currently no documentation on how to write the description files,
# so your best bet is to read through the code and figure it out although that's
# just sub-optimal. 
#
# Pass the descriptor file into the constructor to build the machine, then 
# you can use set_starting_tape to mess with the input tape. When the machine
# is ready, you can use run() to execute until it halts, or use step to move
# the machine cycle by cycle.
#
# Author: Kamil Jarosz
#

class TuringMachine:
    def __init__(self, desc_file):
        self.load_from_file(desc_file)
        self.reset()

    def load_from_file(self, input_machine):
        # Initialize machine properties
        self.init_state = None
        self.final_states = None
        self.transitions = {}
        self.starting_tape = ""

        # Read the file and parse the lines
        with open(input_machine, "r") as i:
            for line in i:
                # Line comments
                if line.startswith("//"):
                    continue

                elif line.startswith("init_state:"):
                    self.init_state = line[len("init_state:"):].strip()
                elif line.startswith("final_states:"):
                    self.final_states = [x.strip() for x in line[len("final_states:"):].split(',')]
                elif line.startswith("["):
                    self.make_transition_function(line)

        # Finish up the loading, report possible errors.
        if not self.init_state:
            raise Exception("Initial state is missing.")

        if not self.final_states:
            raise Exception("Final states are missing.")
                
    def make_transition_function(self, line):
        elements = [x.strip() for x in line.strip().strip('[]').split(',')]
        
        if not len(elements) == 5:
            raise Exception("Invalid transition function: {}".format(line))

        def get_function_operand(index):
            if len(elements[index]) > 0:
                return elements[index]
            raise Exception("Invalid operand.")

        state = get_function_operand(0)
        rsymbol = get_function_operand(1)
        target_state = get_function_operand(2)
        wsymbol = get_function_operand(3)
        move = get_function_operand(4)

        if not (move == "<" or move == ">"):
            raise Exception("Invalid tape move {}.".format(move))

        if not state in self.transitions:
            self.transitions[state] = {}

        if rsymbol in self.transitions[state]:
            raise Exception("Transition for ({}, {}) is defined more than once.".format(state, rsymbol))

        self.transitions[state][rsymbol] = {
            "write": wsymbol,
            "move": self._move_left if move == "<" else self._move_right,
            "target_state": target_state
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
            return

        if not self.read_symbol() in self.transitions[self.current_state]:
            self.halted = True
            return

        transition = self.transitions[state][symbol]

        self.tape = self.tape[:(self.tape_position)] + transition["write"] + self.tape[(self.tape_position+1):]
        transition["move"]()
        self.current_state = transition["target_state"]

    def read_symbol(self):
        return self.tape[self.tape_position] if self.tape_position in range(len(self.tape)) else '_'

    def run(self, print_machine_states=False):
        self.reset()
        self.print_machine()
        while not self.halted:
            self.step()
            if print_machine_states:
                self.print_machine()
        print "Accepted" if self.current_state in self.final_states else "Rejected"
        self.print_machine()

    def print_machine(self):
        tape = [('|{}|'.format(x) if i==self.tape_position else x) for i,x in enumerate(self.tape)]
        print "{} : [ {} ]".format(self.current_state, 
                                   ''.join(tape))
