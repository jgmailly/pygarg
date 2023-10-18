# pygarg: A Python enGine for Argumentation
This program solves most classical problems in abstract argumentation, mainly thanks to calls to SAT solvers. Calls to SAT solvers are made through the PySAT API: https://pysathq.github.io/installation/.

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
