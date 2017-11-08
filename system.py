import re
import sys
import utils as ut
import ope

# Class de noeud contient la lettre du fait et les rules qui lui sont appliqués.
# Les noeuds suivant sont ceux les facts qui se trouvent dans la premières parties des rules.
class Node:
    def __init__(self, lettre, rules):
        self.lettre = lettre
        self.rules = rules
        self.nextNodes = []


# Class de ce que l'on reçoit en entré
class Input:
    def __init__(self, rules, ini, ask):
        self.rules = rules
        self.ini = ini
        self.ask = ask
        self.facts = {}
        self.graph = []

    #print the rules, initialization and question of the input
    def print(self):
        print('rules are:')
        for i, rule in enumerate(self.rules):
            print("#{:d}\t{:s} => {:s}".format(i, rule[0], rule[1]))
        print('TRUE initialized facts: ' + self.ini)
        print('Are these facts TRUE? ' + self.ask)

    #check the order and balance of brackets
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

    #check the logic format of operators and brackets
    def check_logic_format(self):
        for i, rule in enumerate(self.rules):
            for side in rule:
                #no unwanted character
                #unwanted characters before '+^|'
                #unwanted characters after '+^|'
                #unwanted first characters
                #unwanted last characters
                #unwanted characters before '!'
                #unwanted characters after '!'
                #unwanted characters before [A-Z]
                #unwanted characters after [A-Z]
                #check for brackets order and balance
                #check if there are all necessary brackets
                if re.search('[^A-Z()!+|^]', side) != None \
                or re.search('[(!+|^][+^|]', side) != None \
                or re.search('[+^|][)+|^]', side) != None \
                or re.search('^[+^|]', side) != None \
                or re.search('[!+^|]$', side) != None \
                or re.search('[A-Z)]!', side) != None \
                or re.search('![)+|^!]', side) != None \
                or re.search('[)A-Z][A-Z]', side) != None \
                or re.search('[A-Z][!(A-Z]', side) != None \
                or self.check_brackets(side) == False:
                    print('For this set of input:')
                    self.print()
                    ut.exit_m('The format of rule {:d} is non logical'.format(i))

    # On récupère et initialise les facts
    def setFacts(self):
        # Les facts true dans ini
        for c in self.ini:
            if c not in self.facts:
                self.facts[c] = 1

        # Les facts False dans les rules
        for i, lst in enumerate(self.rules):
            for j, tab in enumerate(lst):
                for c in tab:
                    if c.isalpha() and c.isupper() and c not in self.facts:
                        self.facts[c] = 0

        # Les facts False dans ask
        for c in self.ask:
            if c not in self.facts:
                self.facts[c] = 0


    # Algo de backward chaining, on utilise une liste de noeud de facts
    def backwardChaining(self):

        # Liste de Node contient toutes les nodes
        nodeList = []

        # On récupère les rules pour chaque lettre
        dic = {}
        for key in self.facts.keys():
            dic[key] = [x for x in self.rules if key in x[1]]

        # On créer la node pour chaque lettre
        for key, lst in dic.items():
           nodeList.append(Node(key, lst))

        # On relie les nodes entre elles selon les rules
        self.graph = self.linkNodes(nodeList)


        self.resolve()


    def resolve(self):
        
        for querie in self.ask:
            for node in self.graph:
                if node.lettre is querie:
                    

        


    def linkNodes(self, nodeList):
        # On parcours la liste de noeuds
        for node in nodeList:
            # on regarde leurs règles
            for rule in node.rules:
                for c in rule[0]:
                    if c.isalpha() and c.isupper() and self.lettreIsNotInNext(node.nextNodes, c) and c is not node.lettre:
                        for n in nodeList:
                            if n.lettre == c:
                                # on link les noeuds
                                node.nextNodes.append(n)
        return nodeList

    # Vérification de la liste nextNodes return true si il n'existe pas sinon false
    def lettreIsNotInNext(self, lst, c):
        for node in lst:
            if c in node.lettre:
                return False
        return True

    #return 0, 1 or 2 according to the current facts
    def compute_condition(self, cond):
        #if computing fails
        bckup = cond
        #replace by current facts
        s = list(cond)
        for i, l in enumerate(s):
            if l >= 'A' and l <= 'Z':
                s[i] = str(self.facts.get(l))
        cond = "".join(s)
        tmp = ''
        #compute
        while len(cond) > 1 or tmp == cond:
            tmp = cond
            while re.search('[012]\+[012]', cond) != None:
                cond = re.sub('([012])\+([012])', ope.m_and, cond)
            while re.search('[012]\^[012]', cond) != None:
                cond = re.sub('([012])\^([012])', ope.m_xor, cond)
            while re.search('[012]\|[012]', cond) != None:
                cond = re.sub('([012])\|([012])', ope.m_or, cond)
            while re.search('\([012]\)', cond) != None:
                cond = re.sub('\(([012])\)', r'\1', cond)
        #error
        if tmp == cond or (cond != '1' and cond != '2' and cond != '0') :
            exit_m("could not compute the condition '{:s}'".format(bckup))
        return int(cond)


def main():
    import parse as prs
    input = prs.get_parsing()
    input.print()
    input.check_logic_format()
    input.check_logic_format()
    input.setFacts()
    input.compute_condition('(A+B+F+H)|C+D')
    #input.backwardChaining()
if __name__ == '__main__':
    main()
