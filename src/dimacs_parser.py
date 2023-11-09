### Functions for parsing a dimacs file

import sys

# Returns the number of arguments in the AF,
# as defined in the p-line of the file
def parse_p_line(dimacs_line):
    return int(dimacs_line[5:])

# Checks whether a line is empty
def empty_line(line):
    return line == ""

def parse_attack_line(dimacs_line):
    split_line = dimacs_line.split(" ")
    return [split_line[0],split_line[1]]

# Parses a dimacs file and returns the lists of
# arguments and attacks
def parse(filename):
    with open(filename) as dimacsfile:
        dimacs_lines = dimacsfile.read().splitlines()

    nb_args = -1
    args = []
    atts = []
    for dimacs_line in dimacs_lines:
        if dimacs_line[0] == "p":
            nb_args = parse_p_line(dimacs_line)
            args = [str(i+1) for i in range(nb_args)]
        elif not empty_line(dimacs_line) and dimacs_line[0] != "#c":
            atts.append(parse_attack_line(dimacs_line))

    return args, atts

