import parser
import time
import sys
import solvers

import argparse


if len(sys.argv) == 1:
    sys.exit("pygarg v1.0\nJean-Guy Mailly, jean-guy.mailly@u-paris.fr")

semantics_list = ["CF", "AD", "ST", "CO","PR","GR"]
problems_list = ["DC", "DS", "SE", "EE", "CE"]
formats_list = ["apx"]

def print_supported_problems():
    print("[", end='')
    for problem in problems_list:
        for semantics in semantics_list:
            print(f"{problem}-{semantics}", end='')
            if problem != problems_list[-1] or semantics != semantics_list[-1]:
                print(",", end='')
    print("]")

argparser = argparse.ArgumentParser(prog='pygarg', description='A Python enGine for Argumentation: this program solves most classical problems in abstract argumentation, mainly thanks to calls to SAT solvers.')
argparser.add_argument("-p", "--problem", help=f"describes the problem to solve. Must be XX-YY with XX in {problems_list} and YY in {semantics_list}.")
argparser.add_argument("-fo", "--format", help=f"format of the input file. Must be in {formats_list}.", default="apx")
argparser.add_argument("-pr", "--problems", help="prints the list of supported problems.", action="store_true")
argparser.add_argument("-v", "--verbose", help="increase output verbosity.", action="store_true")
argparser.add_argument("-f", "--filename", help=f"the input file describing an AF.")
argparser.add_argument("-a", "--argname", help=f"name of the query argument for acceptability problems.")
cli_args = argparser.parse_args()

if cli_args.problems:
    print_supported_problems()
    sys.exit()

if not cli_args.filename:
    sys.exit("Missing file name.")

if not cli_args.problem:
    sys.exit("Missing problem name.")
    
argname = ""
if cli_args.argname:
    argname = cli_args.argname

apx_file = cli_args.filename
task = cli_args.problem
split_task = task.split("-")
problem = split_task[0]
semantics = split_task[1]

if (problem == "DC" or problem == "DS") and argname == "":
    sys.exit(f"Missing argument name for problem {problem}.")

verbose = False
if cli_args.verbose :
    verbose = True

if problem not in problems_list:
    sys.exit(f"Problem {problem} not recognized. Supported problems: {problems_list}.")

if semantics not in semantics_list:
    sys.exit(f"Semantics {semantics} not recognized. Supported problems: {semantics_list}.")

time_start_parsing = time.time()
args, atts = parser.parse(apx_file)
time_end_parsing = time.time()
duration_parsing = time_end_parsing - time_start_parsing
nb_args = len(args)

if semantics == "GR":
    sys.exit("Grounded semantics is not supported yet.")
    
if problem == "DC":
    time_start_solving = time.time()
    result, extension = solvers.credulous_acceptability(args,atts,argname,semantics)
    time_end_solving = time.time()
    duration_solving = time_end_solving - time_start_solving
    if verbose:
        print(f"{apx_file},{task},",end='')
    if result :
        print("YES")
        solvers.print_witness_extension(extension)
    else:
        print("NO")
    if verbose:
        print(f",{duration_parsing},{duration_solving}")
elif problem == "DS":
    time_start_solving = time.time()
    result = solvers.skeptical_acceptability(args,atts,argname,semantics)
    time_end_solving = time.time()
    duration_solving = time_end_solving - time_start_solving
    if verbose:
        print(f"{apx_file},{task},",end='')
    if result:
        print("YES",end='')
    else:
        print("NO",end='')
    if verbose:
        print(f",{duration_parsing},{duration_solving}")
    else:
        print("")
elif problem == "CE":
    print(solvers.extension_counting(args,atts,semantics))
elif problem == "SE":
    #print(solvers.compute_some_extension(args,atts,semantics))
    extension = solvers.compute_some_extension(args,atts,semantics)
    if extension == "NO":
        print("NO")
    else:
        solvers.print_witness_extension(extension)
elif problem == "EE":
    print(solvers.extension_enumeration(args,atts,semantics))
