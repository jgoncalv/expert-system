import sys
import os.path
import subprocess

def exit_m(message):
    print(message)
    exit()

if len(sys.argv) == 1:
    exit_m("put test file as argument, you can use wildcard '*' to run a battery of tests like 'and_*' or use '*.test' to run all tests")
args = sys.argv[1:]
print()
for arg in args:
    if os.path.isfile(arg):
        h = '\033[33m#####\033[0m {:s} \033[33m#####\033[0m'.format(arg)
        print(h)
        subprocess.run(["cat", arg])
        print()
        subprocess.run(["python3", "../system.py", arg])
        print('\033[33m{:s}\033[0m'.format((len(h) - 18) * '#'))
    else:
        print("File '{:s}' not found".format(arg))
    print()
