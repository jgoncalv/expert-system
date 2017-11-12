#!/usr/bin/python3
import parse
from node import Graph
import sys
import utils as ut

def test_compute_condition(graph):
    print("intermediary results:")
    for rule in graph.rules:
        cond = rule[0]
        result = graph.compute_condition(cond)
        print("{:s}\t= {:d}".format(cond, result))

def main():
    argv = ut.ini_options(sys.argv)
    graph = parse.get_parsing(argv)
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
