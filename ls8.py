import sys
from cpu import *

prog = sys.argv[1]  # Import program

cpu = CPU()  # Initaite class

# Load and run program
cpu.load(prog)
cpu.run()
