import sys
import os.path
import subprocess
import re

def exit_m(message):
    print(message)
    exit()

def check_solution(arg, response):
    ok = 0
    ans = ''
    lines = response.split("\n")
    lines = [l for l in lines if l]
    nb = len(lines)
    for line in lines:
        if re.search("^[A-Z] is true$", line) != None:
            ans = line[0] + '=1'
        elif re.search("^[A-Z] is false$", line) != None:
            ans = line[0] + '=0'
        elif re.search("^[A-Z] is undetermined$", line) != None:
            ans = line[0] + '=2'
        else:
            ok = 0
        solution_file_name = 'solution/' + arg.replace('.test', '.sol')
        if ans != '':
            try:
                with open(solution_file_name, 'r') as f:
                    content = f.read()
                    content = content.replace(" ", "")
                    content = content.split("\n")
                    if ans in content:
                        ok += 1
            except FileNotFoundError:
                print("no solution file, yet...")
    return ok == nb

def main():
    if not os.path.isfile('../Expert_System.py'):
        exit_m('Execute test.py in test directory')
    if len(sys.argv) == 1:
        exit_m("put test file as argument, you can use wildcard '*' to run a battery of tests like 'and_*' or use '*.test' to run all tests")
    args = sys.argv[1:]
    print()
    ok = 0
    for arg in args:
        if os.path.isfile(arg):
            h = '\033[33m#####\033[0m {:s} \033[33m#####\033[0m'.format(arg)
            print(h)
            with open(arg, 'r') as f:
                print(f.read())
            output = subprocess.check_output(["python3", '../Expert_System.py',  arg])
            output = output.decode("utf-8")
            print(output, end='')
            print('\033[33m{:s}\033[0m'.format((len(h) - 18) * '#'))
            test = check_solution(arg, output)
            if test == 1:
                print("\033[32mOK\033[0m")
                ok += 1
            else:
                print("{:s} : \033[31mKO\033[0m".format(arg))
            print()
        else:
            print("File '{:s}' not found".format(arg))
    print("[{:d}/{:d}] tests passed".format(ok, len(args)))

if __name__ == '__main__':
    main()
