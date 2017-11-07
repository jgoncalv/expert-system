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
    
    def check(self):
        for rule in rules:
            if len(rule) != 2:
                exit_m('error in parsing')
