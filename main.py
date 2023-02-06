import parser
#import subprocess
import sys
import solvers
        

semantics_list = ["CF", "AD", "ST", "CO"]
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

if problem not in problems_list:
    sys.exit(f"Problem {problem} not recognized. Supported problems: {problems_list}.")

if semantics not in semantics_list:
    sys.exit(f"Semantics {semantics} not recognized. Supported problems: {semantics_list}.")

args, atts = parser.parse(apx_file)
nb_args = len(args)
    
if problem == "DC":
    if solvers.credulous_acceptability(args,atts,argname,semantics):
        print("YES")
    else:
        print("NO")
elif problem == "DS":
    if solvers.skeptically_acceptability(args,atts,argname,semantics):
        print("YES")
    else:
        print("NO")
elif problem == "CE":
    print(solvers.extension_counting(args,atts,semantics))
elif problem == "SE":
    print(solvers.compute_some_extension(args,atts,semantics))
elif problem == "EE":
    print(solvers.extension_enumeration(args,atts,semantics))
