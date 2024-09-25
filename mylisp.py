import sys
from consolecharstream import ConsoleCharStream
from reader import read_print_loop

if (sys.argv[1] == 'repl'):
    cs = ConsoleCharStream()
    read_print_loop(cs)
