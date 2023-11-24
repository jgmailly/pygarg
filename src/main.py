import apx_parser
import dimacs_parser
import time
import sys
import solvers

import argparse


if len(sys.argv) == 1:
    sys.exit("pygarg - A Python enGine for Argumentation\nv0.1.0\nJean-Guy Mailly, jean-guy.mailly@u-paris.fr")

semantics_list = ["CF", "AD", "ST", "CO","PR","GR", "ID", "SST"]
problems_list = ["DC", "DS", "SE", "EE", "CE", "VE"]
formats_list = ["apx","dimacs"]

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
argparser.add_argument("-fo", "--format", help=f"format of the input file. Must be in {formats_list}.", default="dimacs")
argparser.add_argument("-pr", "--problems", help="prints the list of supported problems.", action="store_true")
#argparser.add_argument("-v", "--verbose", help="increase output verbosity.", action="store_true")
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

af_file = cli_args.filename
task = cli_args.problem
split_task = task.split("-")
problem = split_task[0]
semantics = split_task[1]

if problem == "VE":
    print(argname)
    sys.exit(f"Extension verification is not implemented yet.")

if problem == "VE" and argname == "":
    sys.exit(f"Missing arguments names for problem VE.")
    
if (problem == "DC" or problem == "DS") and argname == "":
    sys.exit(f"Missing argument name for problem {problem}.")

#verbose = False
#if cli_args.verbose :
#    verbose = True

if problem not in problems_list:
    sys.exit(f"Problem {problem} not recognized. Supported problems: {problems_list}.")

if semantics not in semantics_list:
    sys.exit(f"Semantics {semantics} not recognized. Supported problems: {semantics_list}.")

args, atts = [],[]
if cli_args.format == "apx":
    args, atts = apx_parser.parse(af_file)
elif cli_args.format == "dimacs":
    args, atts = dimacs_parser.parse(af_file)
nb_args = len(args)

    
if problem == "DC":
    result, extension = solvers.credulous_acceptability(args,atts,argname,semantics)
    if result :
        print("YES")
        solvers.print_witness_extension(extension)
    else:
        print("NO")
elif problem == "DS":
    result, extension = solvers.skeptical_acceptability(args,atts,argname,semantics)
    if result :
        print("YES")
    else:
        print("NO")
        solvers.print_witness_extension(extension)
elif problem == "CE":
    print(solvers.extension_counting(args,atts,semantics))
elif problem == "SE":
    extension = solvers.compute_some_extension(args,atts,semantics)
    if extension == "NO":
        print("NO")
    else:
        solvers.print_witness_extension(extension)
elif problem == "EE":
    extensions = solvers.extension_enumeration(args,atts,semantics)
    if extensions == []:
        print("NO")
    else:
        for extension in extensions:
            solvers.print_witness_extension(extension)
