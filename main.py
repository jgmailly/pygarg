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

def cred_w_adm(args,atts,argname):
    n_vars, clauses = encoding.conflict_free(args, atts)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
        
    s.add_clause([arg_var])

    while s.solve():
        model = s.get_model()
        extension = argset_from_model(model,args)
        weak_defense = True
        for attacker in encoding.get_attackers(argname,args,atts):
            new_args, new_atts = encoding.reduct(args,atts,extension)
            if (attacker in new_args) and (cred_w_adm(new_args,new_atts,attacker)):
                s.add_clause(negate_model(model))
                weak_defense = False
        if weak_defense:
            return True

    return False
    s.delete()


semantics_list = ["AD_W"]
problems_list = ["DC"]
formats_list = ["apx"]
usage_message=f"Usage: python3 main.py -p <problem>-<semantics> -fo <format> -a <argname> -f <file>\n"
usage_message+=f"Possible semantics: {semantics_list}\n"
usage_message+=f"Possible problems: {problems_list}\n"
usage_message+=f"Possible formats: {formats_list}\n"


if len(sys.argv) != 9:
    sys.exit(usage_message)

argname = sys.argv[6]
apx_file = sys.argv[8]
#semantics = sys.argv[2]


args, atts = parser.parse(apx_file)
nb_args = len(args)

if cred_w_adm(args,atts,argname):
    print("YES")
else:
    print("NO")
