from turing_machine import TuringMachine

tm = TuringMachine("converter.desc")
tm.set_starting_tape("abbaaababaaabaa")
tm.reset()
tm.run(True)

