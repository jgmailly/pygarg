# pygarg: A Python enGine for Argumentation
This program solves most classical problems in abstract argumentation, mainly thanks to calls to SAT solvers. Calls to SAT solvers are made through the PySAT API: https://pysathq.github.io/installation/.

This software is still in development. Any suggestion of improvement
or bug report is welcome: jean-guy.mailly@irit.fr.

pygarg is also available on PyPI (https://pypi.org/project/pygarg/) and can be installed with the command-line:
```bash
pip install pygarg
```

## Command-line Interface
The command-line interface of the current version is as follows:
```bash
usage: pygarg [-h] [-p PROBLEM] [-fo FORMAT] [-pr] [-f FILENAME] [-a ARGNAME]

A Python enGine for Argumentation: this program solves most classical problems in abstract argumentation, mainly thanks to calls to SAT solvers.

options:
  -h, --help            show this help message and exit
  -p PROBLEM, --problem PROBLEM
                        describes the problem to solve. Must be XX-YY with XX in ['DC', 'DS', 'SE', 'EE', 'CE'] and YY in ['CF', 'AD', 'ST', 'CO', 'PR', 'GR', 'ID', 'SST'].
  -fo FORMAT, --format FORMAT
                        format of the input file. Must be in ['apx', 'dimacs'].
  -pr, --problems       prints the list of supported problems.
  -f FILENAME, --filename FILENAME
                        the input file describing an AF.
  -a ARGNAME, --argname ARGNAME
                        name of the query argument for acceptability problems.
```

## Importing pygarg features
You can import pygarg into your own Python script and use its features as follows.

### Text file parsers
```python
import pygarg.dung.apx_parser
import pygarg.dung.dimacs_parser

args, atts = pygarg.dung.apx_parser.parse("test.apx")
args2, atts2 = pygarg.dung.dimacs_parser.parse("test.dimacs")
```

### Extension-based reasoning
```python
import pygarg.dung.solver

for sem in ['CF', 'AD', 'ST', 'CO', 'PR', 'GR', 'ID', 'SST']:
    for argname in args:
        pygarg.dung.solver.credulous_acceptability(args, atts, argname, sem) 
	pygarg.dung.solver.skeptical_acceptability(args, atts, argname, sem) 
    pygarg.dung.solver.compute_some_extension(args, atts, sem) 
    pygarg.dung.solver.extension_enumeration(args, atts, sem) 
    pygarg.dung.solver.extension_counting(args, atts, sem)
```




