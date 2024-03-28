from pygarg.dung import solver, apx_parser
import sys
import time

if len(sys.argv) != 3:
    sys.exit("Usage: python3 experiments.py apxfile semantics")

args, atts = apx_parser.parse(sys.argv[1])
sem = sys.argv[2]

starting_time = time.time()
solver.extension_enumeration(args, atts, sem)
ending_time = time.time()
duration = (ending_time - starting_time) * 1000
    
print(duration)
