import parser
import encoding
import subprocess
import sys
from pysat.solvers import Solver

def argset_from_model(model,args):
    extension = []
    for literal in model:
        int_literal = int(literal)
        if int_literal > 0 and int_literal <= nb_args:
            arg_name = ""
            arg_name = args[int_literal - 1]
            extension.append(arg_name)
    return extension

def negate_model(model):
    negation_clause = []
    for literal in model:
        negation_clause.append(-literal)
    return negation_clause

def get_encoding(args, atts, semantics):
    if semantics == "CF":
        return encoding.conflict_free(args, atts)
    if semantics == "AD":
        return encoding.admissibility(args, atts)
    if semantics == "ST":
        return encoding.stable(args, atts)
    if semantics == "CO":
        return encoding.complete(args, atts)
    sys.exit(f"Unknown semantics : {semantics}")

def credulous_acceptability(args,atts,argname,semantics):
    n_vars, clauses = get_encoding(args, atts,semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
        
    s.add_clause([arg_var])
    
    if s.solve():
        s.delete()
        return True
    s.delete()
    return False

def skeptical_acceptability(args,atts,argname,semantics):
    n_vars, clauses = get_encoding(args, atts,semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
        
    s.add_clause([-arg_var])
    
    if s.solve():
        s.delete()
        return False
    s.delete()
    return True

def compute_some_extension(args,atts,semantics):
    n_vars, clauses = get_encoding(args, atts,semantics)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    if s.solve():
        model = s.get_model()
        s.delete()
        return argset_from_model(model,args)

    return "NO"
        

def extension_enumeration(args,atts,semantics):
    n_vars, clauses = get_encoding(args, atts,semantics)
    extensions = []

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
    
    for model in s.enum_models():
        extensions.append(argset_from_model(model,args))

    s.delete()
    return extensions

def extension_counting(args,atts,semantics):
    return len(extension_enumeration(args,atts,semantics))
        

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
    if credulous_acceptability(args,atts,argname,semantics):
        print("YES")
    else:
        print("NO")
elif problem == "DS":
    if skeptically_acceptability(args,atts,argname,semantics):
        print("YES")
    else:
        print("NO")
elif problem == "CE":
    print(extension_counting(args,atts,semantics))
elif problem == "SE":
    print(compute_some_extension(args,atts,semantics))
elif problem == "EE":
    print(extension_enumeration(args,atts,semantics))
