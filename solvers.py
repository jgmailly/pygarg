from pysat.solvers import Solver
from pysat.examples.lbx import LBX
from pysat.formula import WCNF
import encoding

def argset_from_model(model,args):
    extension = []
    for literal in model:
        int_literal = int(literal)
        if int_literal > 0 and int_literal <= len(args):
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
    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension
    
    if semantics ==  "PR":
        semantics = "AD"
    n_vars, clauses = get_encoding(args, atts,semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
        
    s.add_clause([arg_var])
    
    if s.solve():
        model = s.get_model()
        s.delete()
        return True, argset_from_model(model,args)
    s.delete()
    return False, None


def preferred_skeptical_acceptability(args,atts,argname):
    n_vars, clauses = get_encoding(args, atts,"AD")
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)
        

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        if arg_var in mcs:
            return False, argset_from_model(get_mss_from_mcs(mcs,args),args)

    return True, None


def compute_some_preferred_extension(args,atts):
    n_vars, clauses = get_encoding(args, atts,"AD")

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)
        

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    result = argset_from_model(get_mss_from_mcs(lbx.compute(),args),args)
    lbx.delete()
    return result

def get_unattacked_arguments(args,atts):
    unattacked = []

    for arg in args:
        is_unattacked=True
        for attack in atts:
            if attack[1] == arg:
                is_unattacked = False
        if is_unattacked:
            unattacked.append(encoding.sat_var_from_arg_name(arg,args))

    return unattacked
        

def compute_grounded_extension(args,atts):
    n_vars, clauses = get_encoding(args, atts,"CO")

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    print(f"clauses = {clauses}")

    assump = get_unattacked_arguments(args,atts)
    print(f"assumptions = {assump}")
    status, model = s.propagate(assumptions = assump)
    print(f"model = {model} - status = {status}")
    s.delete()
    return argset_from_model(model,args)

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def intersection_all(args, extensions):
    result = args
    for extension in extensions:
        result = intersection(result, extension)
    return result

def compute_ideal_extension(args, atts):
    preferred_extensions = extension_enumeration(args, atts, "PR")

    skeptical_pr_arguments = intersection_all(args, preferred_extensions)

    n_vars, clauses = get_encoding(args, atts,"AD")

    for arg in args:
        if arg not in skeptical_pr_arguments:
            clauses.append([-encoding.sat_var_from_arg_name(arg, args)])

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)
        

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    result = argset_from_model(get_mss_from_mcs(lbx.compute(),args),args)
    lbx.delete()
    return result


def compute_some_extension(args,atts,semantics):
    if semantics == "PR":
        return compute_some_preferred_extension(args,atts)

    if semantics == "GR":
        return compute_grounded_extension(args,atts)

    if semantics == "ID":
        return compute_ideal_extension(args,atts)
        
    n_vars, clauses = get_encoding(args, atts,semantics)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    if s.solve():
        model = s.get_model()
        s.delete()
        return argset_from_model(model,args)

    return "NO"

def get_mss_from_mcs(mcs,args):
    mss = []
    for arg in args:
        if encoding.sat_var_from_arg_name(arg,args) not in mcs:
            mss.append(encoding.sat_var_from_arg_name(arg,args))
    return mss

def preferred_extension_enumeration(args,atts):
    n_vars, clauses = get_encoding(args, atts,"AD")
    
    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)
        

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    extensions = []
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        extensions.append(argset_from_model(get_mss_from_mcs(mcs,args),args))

    return extensions
        

def extension_enumeration(args,atts,semantics):
    if semantics == "PR":
        return preferred_extension_enumeration(args,atts)
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


def print_witness_extension(extension):
    print("w ", end='')
    for argname in extension:
        print(f"{argname} ", end = '')
    print("")


def skeptical_acceptability(args,atts,argname,semantics):
    if semantics == "PR":
        return preferred_skeptical_acceptability(args,atts,argname)

    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension
    
    n_vars, clauses = get_encoding(args, atts,semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)
        
    s.add_clause([-arg_var])
    
    if s.solve():
        model = s.get_model()
        s.delete()
        return False, argset_from_model(model,args)
    s.delete()
    return True, None
