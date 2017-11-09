import parse as prs
import system
import node

def test_compute_condition(input):
    print("intermediary results:")
    for rule in input.rules:
        cond = rule[0]
        result = input.compute_condition(cond)
        print("{:s}\t= {:d}".format(cond, result))

input = prs.get_parsing()
input.check_logic_format()
input.setFacts()
test_compute_condition(input)
graph = node.Graph(input.rules, input.ini, input.ask)
for q in graph.queries:
    res = graph.facts[q]
    if res == 1:
        print("{} is true".format(q))
    elif res == 0:
        print("{} is false".format(q))
    else:
        print("{} is undetermined".format(q))
