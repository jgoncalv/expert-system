#python3
import utils as ut
import re
from node import Graph

def parse_content(content):
    #get rid of whitespace characters
    content = [re.sub('\s', '', l) for l in content]
    #get rid of comments
    content = [l.split('#')[0] for l in content if l and l[0] != '#']
    rules = []
    tmp = -1
    for i, line in enumerate(content):
        #loop until initialization of facts or questions
        if line[0] == '=' or line[0] == '?':
            tmp = i
            break
        #check unvalid characters
        match = re.search('[^A-Z()!+|^=<>]', line)
        if match != None:
            ut.exit_m("invalid character '{:s}' on line {:d}".format(match.group(), i + 1))
        if re.search('!!', line) != None:
            ut.exit_m("do not put successive '!' on line {:d}".format(i+1))
        #select which 'then' sign 
        if line.count('<=>') > 0:
            sign = '<=>'
        else:
            sign = '=>'
        #check if no 'then' sign
        if line.count(sign) == 0:
            ut.exit_m("No '=>' sign on line {:d}".format(i+1))
        split = line.split(sign)
        #check if too many 'then' sign
        if len(split) > 2:
            ut.exit_m("too many '{:s}' on line {:d}".format(i+1))
        #check before and after 'then' sign
        if split[0] == '' or split[1] == '':
            ut.exit_m("arguments missing on line {:d}".format(i+1))
        #check for characters of the 'then' sign in arguments
        for s in split:
            if re.search('[<=>]', s) != None:
                ut.exit_m("unwanted character on line {:d}".format(i+1))
        #append the rules
        rules.append([split[0], split[1], sign])
    #case of no initialization and questions
    ini = ''
    ask = ''
    if tmp > -1:
        #if there is an initialization line
        if content[tmp][0] == '=':
            ini = content[tmp][1:]
            if re.search('[^A-Z]', ini) != None:
                ut.exit_m("unwanted character on the initialization line")
            if len(content) > tmp + 2:
                ut.exit_m("too many lines after initialization")
            if len(content) == tmp + 2:
                tmp += 1
                if content[tmp][0] != '?':
                    ut.exit_m("you must ask a question after initialization")
        #if there is a question line
        if content[tmp][0] == '?':
            ask = content[tmp][1:]
            if re.search('[^A-Z]', ask) != None:
                ut.exit_m("unwanted character on the question line")
            if len(content) != tmp +1:
                ut.exit_m("the question line should be the last line of input")
    input = Graph(rules, ini, ask)
    return(input)

def get_parsing(argv):
    if len(argv) == 1:
        ut.exit_m('put text file as argument')
    elif len(argv) > 2:
        ut.exit_m('too many arguments')
    try:
        with open(argv[1], 'r') as f:
            #list line by line
            content = f.readlines()
    except FileNotFoundError:
        ut.exit_m('No such file: "' + argv[1] +'"')
    except IsADirectoryError:
        ut.exit_m('Is a directory: "' + argv[1] +'"')
    input = parse_content(content)
    if len(input.rules) == 0:
        if len(input.ask) == 0:
            ut.exit_m('you should ask a question about facts')
    return(input)

if __file__ == 'parse.py':
    input = get_parsing()
    input.print()
    input.check_logic_format()
