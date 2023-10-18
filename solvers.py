import sys 
from pysat.solvers import Solver
from pysat.examples.lbx import LBX
from pysat.examples.mcsls import MCSls
from pysat.formula import WCNF
from pysat.formula import CNF
import encoding

def get_attackers(args,atts,arg):
    attackers = []
    for potential_attacker in args:
        if [potential_attacker, arg] in atts:
            attackers.append(potential_attacker)
    return attackers

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
    sys.exit(f"No SAT encoding for the semantics : {semantics}")

def credulous_acceptability(args,atts,argname,semantics):
    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension

    if semantics == "GR":
        gr_extension = compute_grounded_extension(args,atts)
        if argname in gr_extension:
            return True, gr_extension
        else:
            return False, gr_extension

    if semantics == "SST":
        return semistable_credulous_acceptability(args, atts, argname)
    
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
            unattacked.append(arg)

    return unattacked

def get_defended_set(args, atts, arg_set):
    if arg_set == []:
        return get_unattacked_arguments(args,atts)
    else:
        defended = []
        for arg in args:
            defended_against_all = True
            for attacker in get_attackers(args, atts, arg):
                defenders = get_attackers(args, atts, attacker)
                defended_against_this_one = False
                for defender in defenders:
                    if defender in arg_set:
                        defended_against_this_one = True
                if not defended_against_this_one:
                    defended_against_all = False
            if defended_against_all:
                defended.append(arg)
        return defended
        

def compute_grounded_extension(args,atts):
    extension = []
    defended = get_defended_set(args, atts, extension)

    while defended != extension:
        extension = defended
        defended = get_defended_set(args, atts, extension)

    return extension
    
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

def get_range_mss_from_mcs(mcs,args):
    mss = []
    print(f"mcs = {mcs}")
    for arg in args:
        if encoding.sat_var_from_arg_name(arg,args) not in mcs:
            mss.append(encoding.sat_var_from_arg_name(arg,args))
    print(f"mss = {mss}")
    return mss

def get_extension_from_range(mcs, args):
    mss = get_range_mss_from_mcs(mcs, args)
    extension = []
    for arg in args:
        if encoding.sat_var_from_arg_name(arg,args) in mss:
            extension.append(arg)
    return extension

def compute_some_semistable_extension(args, atts):
    n_vars, clauses = get_encoding(args, atts,"CO")

    soft_clauses = []

    wcnf = WCNF()
    cnf = CNF()
    for clause in clauses:
        cnf.append(clause)
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args), encoding.sat_var_Pa_from_arg_name(argument, args)], weight=1)
        soft_clauses.append([encoding.sat_var_from_arg_name(argument, args), encoding.sat_var_Pa_from_arg_name(argument, args)])
    
    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    mcs = lbx.compute()
    lbx.delete()

    mss = []
    for clause_index in range(1,len(soft_clauses)+1):
        if clause_index not in mcs:
            mss.append(clause_index)
            
    for clause_index in mss:
        cnf.append(soft_clauses[clause_index-1])

    s = Solver(name='g4')
    for clause in cnf.clauses:
        s.add_clause(clause)

    if s.solve():
        model = s.get_model()
        s.delete()
        return argset_from_model(model,args)

    s.delete()
    sys.exit("There cannot be no semi-stable extension.")
    


def compute_some_extension(args,atts,semantics):
    if semantics == "PR":
        return compute_some_preferred_extension(args,atts)

    if semantics == "GR":
        return compute_grounded_extension(args,atts)

    if semantics == "ID":
        return compute_ideal_extension(args,atts)

    if semantics == "SST":
        return compute_some_semistable_extension(args, atts)
        
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


def get_semistable_extensions_from_MCS(args, atts, mcs, hard_clauses, soft_clauses):
    extensions = []

    # Get MSS from MCS
    mss = []
    for clause_index in range(1,len(soft_clauses)+1):
        if clause_index not in mcs:
            mss.append(clause_index)

    # Add the soft clauses from the MSS to the set of hard clauses
    for clause_index in mss:
        hard_clauses.append(soft_clauses[clause_index-1])

    s = Solver(name='g4')
    for clause in hard_clauses:
        s.add_clause(clause)
    
    for model in s.enum_models():
        #print(f"model = {model}")
        extensions.append(argset_from_model(model,args))
        
    return extensions

def semistable_extension_enumeration(args, atts):
    n_vars, clauses = get_encoding(args, atts,"CO")

    soft_clauses = []
    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args),encoding.sat_var_Pa_from_arg_name(argument, args)], weight=1)
        soft_clauses.append([encoding.sat_var_from_arg_name(argument, args), encoding.sat_var_Pa_from_arg_name(argument, args)])
        

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    extensions = []
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        extensions += get_semistable_extensions_from_MCS(args, atts, mcs, clauses, soft_clauses)
    
    lbx.delete()
    
    return extensions

def semistable_skeptical_acceptability(args,atts,argname):
    extensions = semistable_extension_enumeration(args, atts)
    for extension in extensions:
        if argname not in extension:
            return False, extension

    return True, None

def semistable_credulous_acceptability(args,atts,argname):
    extensions = semistable_extension_enumeration(args, atts)
    for extension in extensions:
        if argname in extension:
            return True, extension

    return False, None

def extension_enumeration(args,atts,semantics):
    if semantics == "PR":
        return preferred_extension_enumeration(args,atts)
    if semantics == "ID":
        return [compute_ideal_extension(args,atts)]
    if semantics == "GR":
        return [compute_grounded_extension(args,atts)]
    if semantics == "SST":
        return semistable_extension_enumeration(args, atts)
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
    if semantics == "ID" or semantics == "GR":
        return 1
    return len(extension_enumeration(args,atts,semantics))


def print_witness_extension(extension):
    print("w ", end='')
    for argname in extension:
        print(f"{argname} ", end = '')
    print("")


def skeptical_acceptability(args,atts,argname,semantics):
    if semantics == "PR":
        return preferred_skeptical_acceptability(args,atts,argname)

    if semantics == "SST":
        return semistable_skeptical_acceptability(args, atts, argname)

    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension

    if semantics == "GR":
        gr_extension = compute_grounded_extension(args,atts)
        if argname in gr_extension:
            return True, gr_extension
        else:
            return False, gr_extension
    
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
