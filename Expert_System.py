import parse
from node import Graph
import sys

def test_compute_condition(graph):
    print("intermediary results:")
    for rule in graph.rules:
        cond = rule[0]
        result = graph.compute_condition(cond)
        print("{:s}\t= {:d}".format(cond, result))

def ini_options(argv):
    global OPT_T
    OPT_T = 0
    argv = [arg for arg in argv if arg]
    for arg in argv:
        if arg[0] == '-':
            for l in arg[1:]:
                if l == 't':
                    OPT_T = 1
                else:
                    print("unknow option '{:s}'".format(l))
    return [arg for arg in argv if arg[0] != '-']


def main():
    argv = ini_options(sys.argv)
    rules, inital, queries = parse.get_parsing(argv)
    graph = Graph(rules, initial, queries)
    if OPT_T == 1:
        test_compute_condition(graph)
    for q in graph.queries:
        res = graph.facts[q]
        if res == 1:
            print("{} is true".format(q))
        elif res == 0:
            print("{} is false".format(q))
        else:
            print("{} is undetermined".format(q))

if __name__ == '__main__':
    main()
