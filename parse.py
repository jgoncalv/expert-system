#python3
import sys
import utils as ut
import re

if len(sys.argv) == 1:
    ut.exit_m('put text file as argument')
elif len(sys.argv) > 2:
    ut.exit_m('too many arguments')
try:
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()
except FileNotFoundError:
    ut.exit_m('No such file: "' + sys.argv[1] +'"')
except IsADirectoryError:
    ut.exit_m('Is a directory: "' + sys.argv[1] +'"')
content = [re.sub('\s', '', l) for l in content]
content = [l.split('#')[0] for l in content if l and l[0] != '#']
print(content)
