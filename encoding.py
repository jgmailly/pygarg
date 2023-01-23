import sys

## TO DO
# 1. Encode admissibility
# 2. Encode completeness
# 3. Encode stability
# 4. In another module, encode resolution of problems DC, DS, SE, EE, CE


## args[i] -> i+1


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

# Returns the set of attackers of an argument
def get_attackers(argument, args, atts):
    attackers = []
    for attack in atts:
        if (attack[1] == argument) and (attack[0] in args):
            attackers.append(attack[0])
    return attackers



##### Encodes conflict-freeness
def conflict_free(args, atts):
    clauses = []
    n_vars = len(args)
    for attack in atts:
        attacker = attack[0]
        target = attack[1]
        if (attacker in args) and (target in args):
            new_clause = [-sat_var_from_arg_name(attacker, args), -sat_var_from_arg_name(target, args)]
            clauses.append(new_clause)

    return n_vars, clauses





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
