# Functions for parsing an apx file

import sys


def parse_arg(apx_line):
    """Provide the name of an argument identified in the apx file."""
    return apx_line[4:-2]


def parse_att(apx_line):
    """Provide the names of arguments in an attack."""
    arg_names = apx_line[4:-2]
    return arg_names.split(",")


def empty_line(apx_line):
    """Check if a line is empty."""
    return apx_line == ""


def parse(filename):
    """Parse an apx file and returns the lists of arguments and attacks."""
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
