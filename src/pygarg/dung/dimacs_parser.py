# Functions for parsing a dimacs file


def parse_p_line(dimacs_line):
    """Provide the number of arguments in the AF from p-line of the file."""
    return int(dimacs_line[5:])


def empty_line(line):
    """Check whether a line is empty."""
    return line == ""


def parse_attack_line(dimacs_line):
    """Provide the arguments involved in an attack."""
    split_line = dimacs_line.split(" ")
    return [split_line[0], split_line[1]]


def parse(filename):
    """Parse a dimacs file and returns the lists of arguments and attacks."""
    with open(filename) as dimacsfile:
        dimacs_lines = dimacsfile.read().splitlines()

    nb_args = -1
    args = []
    atts = []
    for dimacs_line in dimacs_lines:
        if dimacs_line[0] == "p":
            nb_args = parse_p_line(dimacs_line)
            args = [str(i+1) for i in range(nb_args)]
        elif not empty_line(dimacs_line) and dimacs_line[0] != "#":
            atts.append(parse_attack_line(dimacs_line))

    return args, atts
