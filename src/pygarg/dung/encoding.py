import sys

# args[i] -> i+1
# P(args[i]) -> n + (i+1) : means that one attacker of args[i]
# is in the extension
# Q(args[i]) -> 2n + (i+1) : means that args[i]
# is in the range of the extension


def attacked_by(arg, set_of_args, atts):
    """Determine whether an argument is attacked by a set.

    Arguments:
    arg -- the query argument
    set_of_args -- the potential attackers
    atts -- the attacks in the AF
    """
    for possible_attacker in set_of_args:
        if [possible_attacker, arg] in atts:
            return True
    return False


def sat_var_from_arg_name(argname, args):
    """Provide the integer corresponding to an argument.

    Useful for building clauses to feed the SAT solver.
    Arguments:
    argname -- the name of the argument
    args -- the arguments in the AF
    """
    if argname in args:
        return args.index(argname) + 1
    else:
        sys.exit(f"Unknown argument name: ({argname})")


def sat_var_Pa_from_arg_name(argname, args):
    """Provide the integer for Pa variables.

    Pa is true means that one attacker of a is in the extension.
    Arguments:
    argname -- the argument
    args -- the arguments in the AF
    """
    if argname in args:
        return args.index(argname) + 1 + len(args)
    else:
        sys.exit(f"Unkown argument name: ({argname})")


def sat_var_Qa_from_arg_name(argname, args):
    """Provide the integer for Qa variables.

    Qa is true means that a is in the range of the extension.
    Arguments:
    argname -- the argument
    args -- the arguments in the AF
    """
    if argname in args:
        return args.index(argname) + 1 + 2 * len(args)
    else:
        sys.exit(f"Unkown argument name: ({argname})")


def get_attackers(argument, args, atts):
    """Provide the set of attackers of an argument."""
    attackers = []
    for attack in atts:
        if (attack[1] == argument) and (attack[0] in args):
            attackers.append(attack[0])
    return attackers


# For each a, Qa <-> a or Pa. In clauses:
# (-Qa or a or Pa), (-a or Qa), (-Pa or Qa)
def encode_range_variables(args, atts):
    """Encode the meaning of range variables."""
    clauses = []

    for arg in args:
        clauses.append([-sat_var_Qa_from_arg_name(arg, args),
                       sat_var_from_arg_name(arg, args),
                       sat_var_Pa_from_arg_name(arg, args)])
        clauses.append([-sat_var_from_arg_name(arg, args),
                       sat_var_Qa_from_arg_name(arg, args)])
        clauses.append([-sat_var_Pa_from_arg_name(arg, args),
                       sat_var_Qa_from_arg_name(arg, args)])

    return 3*len(args), clauses


def conflict_free(args, atts):
    """Encode conflict-freeness."""
    clauses = []
    n_vars = len(args)
    for attack in atts:
        attacker = attack[0]
        target = attack[1]
        new_clause = [-sat_var_from_arg_name(attacker, args),
                      -sat_var_from_arg_name(target, args)]
        clauses.append(new_clause)

    return n_vars, clauses


def stable(args, atts):
    """Encode stable semantics."""
    n_vars, clauses = conflict_free(args, atts)
    for argument in args:
        new_clause = [sat_var_from_arg_name(argument, args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause.append(sat_var_from_arg_name(attacker, args))
        clauses.append(new_clause)
    return n_vars, clauses


def pa_vars(args, atts):
    """Encode Pa variables for defense."""
    clauses = []
    n_vars = len(args)*2
    for argument in args:
        long_clause = [-sat_var_Pa_from_arg_name(argument, args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(argument, args),
                          -sat_var_from_arg_name(attacker, args)]
            clauses.append(new_clause)
            long_clause.append(sat_var_from_arg_name(attacker, args))
        clauses.append(long_clause)
    return n_vars, clauses


def defense(args, atts):
    """Encode defense."""
    n_vars, clauses = pa_vars(args, atts)
    for argument in args:
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(attacker, args),
                          -sat_var_from_arg_name(argument, args)]
            clauses.append(new_clause)
    return n_vars, clauses


def admissibility(args, atts):
    """Encode admissibility."""
    n_vars, cf_clauses = conflict_free(args, atts)
    def_clauses = defense(args, atts)[1]
    return n_vars, cf_clauses + def_clauses


def complete_defense(args, atts):
    """Encode full defense for the complete semantics."""
    n_vars, clauses = pa_vars(args, atts)
    for argument in args:
        long_clause = [sat_var_from_arg_name(argument, args)]
        for attacker in get_attackers(argument, args, atts):
            new_clause = [sat_var_Pa_from_arg_name(attacker, args),
                          -sat_var_from_arg_name(argument, args)]
            clauses.append(new_clause)
            long_clause.append(-sat_var_Pa_from_arg_name(attacker, args))
        clauses.append(long_clause)
    return n_vars, clauses


def complete(args, atts):
    """Encode complete semantics."""
    n_vars, cf_clauses = conflict_free(args, atts)
    def_clauses = complete_defense(args, atts)[1]
    return n_vars, cf_clauses + def_clauses


def write_dimacs_clause(clause):
    """Provide the string representation of a clause in Dimacs format."""
    dimacs_clause = ""
    for literal in clause:
        dimacs_clause += (str(literal) + " ")
    dimacs_clause += "0\n"
    return dimacs_clause


def print_extension(extension):
    "Print an extension to the standard output."""
    if extension == []:
        print("[]")
    else:
        print("[", end="")
        for i in range(len(extension) - 1):
            print(f"{extension[i]},", end="")
        print(f"{extension[len(extension)-1]}]")
