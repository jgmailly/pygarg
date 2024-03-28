from dung import apx_parser, dimacs_parser, solver
import sys

import argparse

software_version = "v0.1.1"
author_id = "Jean-Guy Mailly, jean-guy.mailly@irit.fr"

if len(sys.argv) == 1:
    error_message = "pygarg - A Python enGine for Argumentation\n"
    error_message += software_version + "\n"
    error_message += author_id
    sys.exit(error_message)

semantics_list = ["CF",  "AD",  "ST",  "CO", "PR", "GR", "ID", "SST"]
problems_list = ["DC", "DS", "SE", "EE", "CE"]
formats_list = ["apx", "dimacs"]


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
argparser.add_argument("-f", "--filename", help="the input file describing an AF.")
argparser.add_argument("-a", "--argname", help="name of the query argument for acceptability problems.")
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

if (problem == "DC" or problem == "DS") and argname == "":
    sys.exit(f"Missing argument name for problem {problem}.")

if problem not in problems_list:
    error_message = f"Problem {problem} not recognized. "
    error_message += f"Supported problems: {problems_list}."
    sys.exit(error_message)

if semantics not in semantics_list:
    error_message = f"Semantics {semantics} not recognized. "
    error_message += f"Supported problems: {semantics_list}."
    sys.exit(error_message)

args, atts = [], []
if cli_args.format == "apx":
    args, atts = apx_parser.parse(af_file)
elif cli_args.format == "dimacs":
    args, atts = dimacs_parser.parse(af_file)
nb_args = len(args)


if problem == "DC":
    result, extension = solver.credulous_acceptability(args, atts,
                                                        argname, semantics)
    if result:
        print("YES")
        solver.print_witness_extension(extension)
    else:
        print("NO")
elif problem == "DS":
    result, extension = solver.skeptical_acceptability(args, atts,
                                                        argname, semantics)
    if result:
        print("YES")
    else:
        print("NO")
        solver.print_witness_extension(extension)
elif problem == "CE":
    print(solver.extension_counting(args, atts, semantics))
elif problem == "SE":
    extension = solver.compute_some_extension(args, atts, semantics)
    if extension == "NO":
        print("NO")
    else:
        solver.print_witness_extension(extension)
elif problem == "EE":
    extensions = solver.extension_enumeration(args, atts, semantics)
    if extensions == []:
        print("NO")
    else:
        for extension in extensions:
            solver.print_witness_extension(extension)
