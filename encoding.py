import sys



## args[i] -> i+1
## P(args[i]) -> n + (i+1) : means that one attacker of args[i] is in the extension
## Q(args[i]) -> 2n + (i+1) : means that args[i] is in the range of the extension


# Determines whether arg is attacked by a member of
# set_of_args w.r.t. the attack relation atts
def attacked_by(arg,set_of_args,atts):
    for possible_attacker in set_of_args:
        if [possible_attacker, arg] in atts:
            return True
    return False


# Returns the integer value corresponding to an argument name
# Useful for building clauses to feed the SAT solver
def sat_var_from_arg_name(argname, args):
    if argname in args:
        return args.index(argname) + 1
    else:
        sys.exit(f"Unknown argument name: ({argname})")

def sat_var_Pa_from_arg_name(argname, args):
    if argname in args:
        return args.index(argname) + 1 + len(args)
    else:
        sys.exit(f"Unkown argument name: ({argname})")

def sat_var_Qa_from_arg_name(argname, args):
    if argname in args:
        return args.index(argname) + 1 + 2 * len(args)
    else:
        sys.exit(f"Unkown argument name: ({argname})")

# Returns the set of attackers of an argument
def get_attackers(argument, args, atts):
    attackers = []
    for attack in atts:
        if (attack[1] == argument) and (attack[0] in args):
            attackers.append(attack[0])
    return attackers

#### Encodes range variables
def encode_range_variables(args, atts):
    clauses = []
    n_vars = len(args) * 3
    for argument in args:
        clauses.append([-sat_var_from_arg_name(argument, args), sat_var_Qa_from_arg_name(argument, args)])
        long_clause = [-sat_var_Qa_from_arg_name(argument, args), sat_var_from_arg_name(argument, args)]
        for attacker in args:
            if [attacker, argument] in atts:
                clauses.append([-sat_var_from_arg_name(attacker, args), sat_var_Qa_from_arg_name(argument, args)])
                long_clause.append(sat_var_from_arg_name(attacker, args))
        clauses.append(long_clause)
    return n_vars, clauses


##### Encodes conflict-freeness
def conflict_free(args, atts):
    clauses = []
    n_vars = len(args)
    for attack in atts:
        attacker = attack[0]
        target = attack[1]
        new_clause = [-sat_var_from_arg_name(attacker, args), -sat_var_from_arg_name(target, args)]
        clauses.append(new_clause)
            
    return n_vars, clauses


##### Encodes stable semantics
def stable(args, atts):
    n_vars, clauses = conflict_free(args, atts)
    for argument in args:
        new_clause = [sat_var_from_arg_name(argument,args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause.append(sat_var_from_arg_name(attacker, args))
        clauses.append(new_clause)
    return n_vars, clauses

#### Encodes defense
def pa_vars(args,atts):
    clauses = []
    n_vars = len(args)*2
    for argument in args:
        long_clause = [-sat_var_Pa_from_arg_name(argument, args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(argument, args), -sat_var_from_arg_name(attacker, args)]
            clauses.append(new_clause)
            long_clause.append(sat_var_from_arg_name(attacker, args))
        clauses.append(long_clause)
    return n_vars, clauses

def defense(args, atts):
    n_vars, clauses = pa_vars(args, atts)
    for argument in args:
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(attacker, args), -sat_var_from_arg_name(argument, args)]
            clauses.append(new_clause)
    return n_vars, clauses
    

### Encodes admissibility
def admissibility(args, atts):
    n_vars, cf_clauses = conflict_free(args, atts)
    def_clauses = defense(args, atts)[1]
    return n_vars, cf_clauses + def_clauses

### Encodes complete semantics
def complete_defense(args, atts):
    n_vars, clauses = pa_vars(args, atts)
    for argument in args:
        long_clause = [sat_var_from_arg_name(argument,args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(attacker, args), -sat_var_from_arg_name(argument, args)]
            clauses.append(new_clause)
            long_clause.append(-sat_var_Pa_from_arg_name(attacker, args))
        clauses.append(long_clause)
    return n_vars, clauses

def complete(args, atts):
    n_vars, cf_clauses = conflict_free(args, atts)
    def_clauses = complete_defense(args, atts)[1]
    return n_vars, cf_clauses + def_clauses


##### Encoding generation
# Returns the string representation of a clause
# in Dimacs format
def write_dimacs_clause(clause):
    dimacs_clause = ""
    for literal in clause:
        dimacs_clause += (str(literal) + " ")
    dimacs_clause += "0\n"
    return dimacs_clause



# Prints an extension to the standard output
def print_extension(extension):
    if extension == []:
        print("[]")
    else:
        print("[", end="")
        for i in range(len(extension) - 1):
            print(f"{extension[i]},", end="")
        print(f"{extension[len(extension)-1]}]")
