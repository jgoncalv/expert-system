import re
import sys

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
        
        # Node list contient toutes les nodes
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
        print(self.graph)

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


def main():
    input = Input([ ['A', 'B'], ['C', 'D']], 'ABD', 'HD')
    input.setFacts()
    input.backwardChaining()



if __name__ == '__main__':
    main()	