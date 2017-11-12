#!/usr/bin/python3
def exit_m(message):
    print(message)
    exit()

def ini_options(argv):
    global OPT_C
    global OPT_V
    OPT_C = 0
    OPT_V = 0
    argv = [arg for arg in argv if arg]
    for arg in argv:
        if arg[0] == '-':
            for l in arg[1:]:
                if l == 'v':
                    OPT_V = 1
                elif l == 'c':
                    OPT_C = 1
                else:
                    print("unknown option '{:s}'".format(l))
    return [arg for arg in argv if arg[0] != '-']

def verbose(message):
    if OPT_V == 1:
        print(message)
