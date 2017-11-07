import re
import utils as ut

class Input:
    def __init__(self, rules, ini, ask):
        self.rules = rules
        self.ini = ini
        self.ask = ask

    def print(self):
        print('rules are:')
        for i, rule in enumerate(self.rules):
            print("#{:d}\t{:s} => {:s}".format(i, rule[0], rule[1]))
        print('TRUE initialized facts: ' + self.ini)
        print('Are these facts TRUE? ' + self.ask)
    
    def check_brackets(self, side):
        br = []
        for i, l in enumerate(side):
            if l == '(':
                br.append(i)
            elif l == ')':
                if len(br) == 0:
                    return False
                else:
                    br.pop()
        return len(br) == 0

    def check_logic_format(self):
        for i, rule in enumerate(self.rules):
            for side in rule:
                if re.search('[^A-Z()!+|^]', side) != None \
                or re.search('[(!+|^][+^|]', side) != None \
                or re.search('[+^|][)+|^]', side) != None \
                or re.search('^[+^|]', side) != None \
                or re.search('[!+^|]$', side) != None \
                or re.search('[A-Z)]!', side) != None \
                or re.search('![)+|^!]', side) != None \
                or self.check_brackets(side) == False:
                    print('For this set of input:')
                    self.print()
                    ut.exit_m('The format of rule {:d} is non logical'.format(i))

