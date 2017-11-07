#python3
import sys
import utils as ut
import re

class Input:
    def __init__(self, rules, ini, ask):
        self.rules = rules
        self.ini = ini
        self.ask = ask

    def print(self):
        print('rules are:')
        for rule in self.rules:
            print('{:s} => {:s}'.format(rule[0], rule[1]))
        print('TRUE initialized facts: ' + self.ini)
        print('Are these facts TRUE? ' + self.ask)

def parse_content(content):
    content = [re.sub('\s', '', l) for l in content]
    content = [l.split('#')[0] for l in content if l and l[0] != '#']
    rules = []
    for i, line in enumerate(content):
        if line[0] == '=':
            tmp = i
            break
        match = re.search('[^A-Z()!+|^=<>]', line)
        if match != None:
            ut.exit_m("invalid character '{:s}' on line {:d}".format(match.group(), i + 1))
        if line.count('=>') == 0:
            ut.exit_m("No '=>' sign on line {:d}".format(i + 1))
        if line.count('=>') > 1:
            ut.exit_m("too many '=>' signs on line {:d}".format(i+1))
        split = line.split('=>')
        if len(split) != 2 or split[0] == '' or split[1] == '':
            ut.exit_m("arguments missing on line {:d}".format(i+1))
        if re.search('<', line) != None and re.search('<=>', line) == None:
            ut.exit_m("Misplaced '<' on line {:d}".format(i+1))
        if '<=>' in line:
            split = line.split('<=>')
            rules.append([split[0], split[1]])
            rules.append([split[1], split[0]])
        else:
            rules.append([split[0], split[1]])
    ini = content[i][1:]
    ask = content[i+1][1:]
    input = Input(rules, ini, ask)
    return(input)

def get_parsing():
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
    input = parse_content(content)
    return(input)

if __file__ == 'parse.py':
    input = get_parsing()
    input.print()
