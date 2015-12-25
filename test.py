from turing_machine import TuringMachine

tm = TuringMachine("test_machine.desc")
tm.set_starting_tape("BabbaaababaaabaaB")
tm.reset()
tm.run()

