import parser
import time
import sys
import solvers
        

semantics_list = ["CF", "AD", "ST", "CO","PR","GR"]
problems_list = ["DC", "DS", "SE", "EE", "CE"]
formats_list = ["apx"]
usage_message=f"Usage: python3 main.py -p <problem>-<semantics> -fo <format> -f <file> [-a <argname>]\n"
usage_message+=f"Possible semantics: {semantics_list}\n"
usage_message+=f"Possible problems: {problems_list}\n"
usage_message+=f"Possible formats: {formats_list}\n"

argname = ""
if len(sys.argv) > 7:
    argname = sys.argv[8]
apx_file = sys.argv[6]
task = sys.argv[2]
split_task = task.split("-")
problem = split_task[0]
semantics = split_task[1]

verbose = False
if "-v" in sys.argv or "--verbose" in sys.argv:
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
    result = solvers.credulous_acceptability(args,atts,argname,semantics)
    time_end_solving = time.time()
    duration_solving = time_end_solving - time_start_solving
    if result :
        print("YES",end='')
    else:
        print("NO",end='')
    if verbose:
        print(f",{duration_parsing},{duration_solving}")
    else:
        print("")
elif problem == "DS":
    time_start_solving = time.time()
    result = solvers.skeptical_acceptability(args,atts,argname,semantics)
    time_end_solving = time.time()
    duration_solving = time_end_solving - time_start_solving
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
    print(solvers.compute_some_extension(args,atts,semantics))
elif problem == "EE":
    print(solvers.extension_enumeration(args,atts,semantics))
