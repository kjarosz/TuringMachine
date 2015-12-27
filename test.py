from turing_machine import TuringMachine

print "Testing converter (abbaaababaaabaa -> bbbbbbbbbbbbbbb)" 
tm = TuringMachine("converter.desc")
tm.set_starting_tape("abbaaababaaabaa")
tm.reset()
tm.run(True)

print ""
print "Testing matcher (Expecting acceptance)"
tm = TuringMachine("matcher.desc")
tm.set_starting_tape("BaaaabbbbccccB")
tm.reset()
tm.run(True)

print ""
print "Testing matcher (Expecting rejection)"
tm.set_starting_tape("BaaaabbbbcccB")
tm.reset()
tm.run(True)
