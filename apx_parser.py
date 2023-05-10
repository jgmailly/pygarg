### Functions for parsing an apx file

import sys


# Returns the name of a certain argument
# identified in an apx line
def parse_arg(apx_line):
    return apx_line[4:-2]


# Returns the names of the arguments in a certain attack
# identified in an apx line
def parse_att(apx_line):
    arg_names = apx_line[4:-2]
    return arg_names.split(",")

def empty_line(apx_line):
    return apx_line == ""

# Parses an apx file and returns the lists of
# certain arguments, uncertain arguments, certain attacks and uncertain attacks
def parse(filename):
    with open(filename) as apxfile:
        apx_lines = apxfile.read().splitlines()

    args = []
    atts = []
    for apx_line in apx_lines:
        if apx_line[0:3] == "arg":
            args.append(parse_arg(apx_line))
        elif apx_line[0:3] == "att":
            atts.append(parse_att(apx_line))
        elif not empty_line(apx_line):
            sys.exit(f"Line cannot be parsed ({apx_line})")

    return args, atts

