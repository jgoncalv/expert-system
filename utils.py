def exit_m(message):
    print(message)
    exit()

def ini_options(argv):
    global OPT_T
    global OPT_C
    OPT_C = 0
    OPT_T = 0
    argv = [arg for arg in argv if arg]
    for arg in argv:
        if arg[0] == '-':
            for l in arg[1:]:
                if l == 't':
                    OPT_T = 1
                if l == 'c':
                    OPT_C = 1
                else:
                    print("unknow option '{:s}'".format(l))
    return [arg for arg in argv if arg[0] != '-']
