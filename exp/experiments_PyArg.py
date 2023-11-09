import sys
import time

from py_arg.import_export.argumentation_framework_from_aspartix_format_reader import ArgumentationFrameworkFromASPARTIXFormatReader
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions
from py_arg.algorithms.semantics.get_preferred_extensions import get_preferred_extensions
from py_arg.algorithms.semantics.get_stable_extensions import get_stable_extensions
from py_arg.algorithms.semantics.get_semistable_extensions import get_semistable_extensions
from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension
from py_arg.algorithms.semantics.get_ideal_extension import get_ideal_extension




if len(sys.argv) != 3:
    sys.exit("Usage: python3 experiments.py apxfile semantics")

lines = []
with open(sys.argv[1]) as f:
    lines += [line.rstrip() for line in f]

apx_lines = ""
for line in lines:
    apx_lines += line

af = ArgumentationFrameworkFromASPARTIXFormatReader.from_apx(apx_lines)

sem = sys.argv[2]

starting_time = time.time()
if sem == "CO":
    get_complete_extensions(af)
if sem =="GR":
    get_grounded_extension(af)
if sem == "PR":
    get_preferred_extensions(af)
if sem == "ST":
    get_stable_extensions(af)
if sem == "SST":
    get_semistable_extensions(af)
if sem == "ID":
    get_ideal_extension(af)
ending_time = time.time()
duration = (ending_time - starting_time) * 1000
    
print(duration)
