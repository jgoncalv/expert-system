import re
import utils as ut
"""
    NOUVEAU GRAPH
"""
class Fact:
    def __init__(self, fact):
        self.fact = fact
        # contient les noeuds des rule qui implique ce fact
        self.rules = []


class Rule:
    def __init__(self, rule):
        self.rule = rule
        # contient les noeuds facts dans la premiere partie de rule
        self.firstFacts = []
        # contient les noeuds facts dans la seconde partie
        self.secondFacts = []



class Graph:
    def __init__(self, rules, initial, queries):
        self.rules = rules
        self.initial = initial
        self.queries = queries
        self.facts = {}
        self.graph = []
        self.ruleNodes = []
        self.factNodes = []
        self.objectivesFacts = []
        self.nodeChecked = []


        ### Vérification
        self.check_logic_format()
        ###


        ### On Créer le Graphe
        self.setFacts()
        self.createNodes()
        self.linkRulesAndFacts()
        self.createQuerieGraph()
        ###

        ### On éxecute le backwar chaining
        self.backwardChaining()
        ###



    #print the rules, initialization and question of the input
    def display(self):
        print('rules are:')
        for i, rule in enumerate(self.rules):
            print("#{:d}\t{:s} => {:s}".format(i, rule[0], rule[1]))
        print('TRUE initialized facts: ' + self.initial)
        print('Are these facts TRUE? ' + self.queries)

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
            r = rule[:2]
            for side in r:
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
                    self.display()
                    ut.exit_m('The format of rule {:d} is non logical'.format(i))



    # On récupère et initialise les facts
    def setFacts(self):
        # Les facts true dans ini
        for c in self.initial:
            if c not in self.facts:
                self.facts[c] = True
        # Les facts False dans les rules
        for i, lst in enumerate(self.rules):
            for j, tab in enumerate(lst):
                for c in tab:
                    if c.isalpha() and c.isupper() and c not in self.facts:
                        self.facts[c] = False
        # Les facts False dans ask
        for c in self.queries:
            if c not in self.facts:
                self.facts[c] = False

    # On créer les noeud ruleNodes et factNodes
    def createNodes(self):
        for rule in self.rules:
            self.ruleNodes.append(Rule(rule))
        for fact in self.facts.keys():
            self.factNodes.append(Fact(fact))

    # Relie les rules et les facts entre eux
    def linkRulesAndFacts(self):
        for rule in self.ruleNodes:
            for c in rule.rule[0]:
                for fact in self.factNodes:
                    if fact.fact is c:
                        rule.firstFacts.append(fact)
            for c in rule.rule[1]:
                for fact in self.factNodes:
                    if fact.fact is c:
                        rule.secondFacts.append(fact)
        # Fact est relié avec les règles auxquel elle est appliqué
        for factNode in self.factNodes:
            for rule in self.ruleNodes:
                for fact in rule.secondFacts:
                    if factNode is fact:
                        factNode.rules.append(rule)
                for fact in rule.firstFacts:
                    if (factNode is fact) and (rule.rule[2] == '<=>'):
                        factNode.rules.append(rule)

    # On créer le nouveau graph selon les queries
    def createQuerieGraph(self):
        for querie in self.queries:
            for factNode in self.factNodes:
                if factNode.fact is querie:
                    self.graph.append(factNode)

    # Vérifie si il n'est pas déjà dans la liste et l'ajoute
    def addNodeCheck(self, fact):
        isIn = False
        for n in self.nodeChecked:
            if n is fact:
                isIn = True
                break
        if isIn == False:
            self.nodeChecked.append(fact)

    '''
        Permet de réaliser une liste d'objectif selon si un noeud fact est true ou non
        et tente de résoudre les rules en prenant en compte 
    '''
    def backwardChaining(self):

        self.checkInconsistency()

        # On rajoute dans nodeChecked les facts qui n'ont pas de rules
        for fact in self.factNodes:
            #if not fact.rules ''' or self.facts[fact.fact] == True''':
            if not fact.rules:
                self.addNodeCheck(fact)

        # On rajoute les nouveaux objectifs récursivement
        for fact in self.graph:
            if fact not in self.nodeChecked:
                self.objectivesFacts.append(fact)
                self.getObjectivesRecursiveRules(fact.rules)

        self.checkInconsistency()

        # Maintenant qu'on a la liste il faut résoudre les équations de chaque facts en partant du bas de la liste
        while (self.objectivesFacts):
            i = len(self.objectivesFacts) - 1
            while (i >= 0 and self.objectivesFacts):
                res = self.resolve(self.objectivesFacts[i])
                self.checkInconsistency()
                if res == True:
                    # On a trouvé un true donc on recommence du début
                    i = len(self.objectivesFacts) - 1
                elif i == 0:
                    # Comme on a pas trouvé de solution on supprime le dernier fact de la liste
                    l = len(self.objectivesFacts) - 1
                    f = self.objectivesFacts[l]
                    self.addNodeCheck(f)
                    self.objectivesFacts.remove(f)
                else:
                    i -= 1

    # On regarde si il y a une incoherence entre differete regle lier a une regle
    def checkInconsistency(self):
        dic = self.getFactUnknown()
        for fact in self.factNodes:
            self.computeCondition(fact.rules, dic)

    def getFactUnknown(self):
        dic = {}
        for fact in self.nodeChecked:
            if fact.fact in self.facts.keys():
                dic[fact.fact] = self.facts[fact.fact]
        for key, value in self.facts.items():
            if key not in dic.keys():
                if value == True:
                    dic[key] = value
                elif value == False:
                    dic[key] = None
        return dic

    def computeCondition(self, rules, dic):
        r1 = None
        r2 = None
        for rule in rules:
            for c in rule.rule[0]:
                if c in dic.keys() and dic[c] == True:
                    r1 = self.compute(rule.rule[0], dic)
            for c in rule.rule[1]:
                if c in dic.keys() and dic[c] == True:
                    r2 = self.compute(rule.rule[1], dic)
            if r1 != r2 and r1 != None and r2 != None:
                tab = []
                for x in rules:
                    s = x.rule[0] + x.rule[2] + x.rule[1]
                    tab.append(s)
                exit("Il y a une incoherence. {} avec {}.".format(tab, dic))

    def compute(self, cond, dic):
        lst = list(cond)
        for i, c in enumerate(lst):
            if c in dic.keys():
                lst[i] = str(dic[c])
            elif c == '+':
                lst[i] = "and"
            elif c == '|':
                lst[i] = "or"
            elif c == '^':
                lst[i] = "!="
            elif c == '!':
                lst[i] = str("not")
            else:
                lst[i] = c
        s = ' '.join(lst)
        return eval(s)

    #compute recursively all permutations of [False/True] elements in a list of size n
    def rec_p(self, n):
        all = []
        all.append([False] * n)
        j = 0
        while j < n:
            poss = [False] * (j + 1)
            poss[j] = True
            rest = self.rec_p(n - (j+1))
            for r in rest:
                all.append(poss + r)
            j += 1
        return all
   
    #if there is an operator in the right side of a rule, prompt a choice to the user
    def user_choice(self, rule, res, unknown, perm):
        print("{:s} {:s} {:s}".format(rule[0], rule[2], rule[1]))
        print("'{:s}' is {}, for '{:s}' to be {} you can choose between:".format(rule[0], res, rule[1], res))
        for n, p in enumerate(perm):
            opt = ''
            for i, f in enumerate(p):
                opt += ' {} is {} &'.format(unknown[i], f)
            if opt:
                opt = opt[:-1]
            print("{:d}){:s}".format(n + 1, opt))
        nb = ''
        while nb.isdigit() != True or int(nb) <= 0 or int(nb) > len(perm):
            nb = input('Enter the number of an option: ')
        nb = int(nb)
        chosen_opt = perm[nb - 1]
        return chosen_opt

    #test all options that could fit the final value of the right side of the rule
    def test_all(self, res, rule, dic):
        unknown = []
        perm = []
        cond = rule[1]
        for l in cond:
            if l in dic.keys():
                unknown.append(l)
        all = self.rec_p(len(unknown))
        for p in all:
            for i, v in enumerate(p):
                dic[unknown[i]] = v
            if res == self.compute(cond, dic):
                perm.append(p)
        if len(perm) == 0:
            if res == True:
                ut.exit_m("Incoherence: '{:s}' is {} and '{:s}' cannot be {}".format(rule[0], res, cond, res))
            else:
                return False
        elif len(perm) == 1:
            chosen_opt = perm[0]
        else:
            if ut.OPT_C == 0:
               return False
            chosen_opt = self.user_choice(rule, res, unknown, perm)
        for i, v in  enumerate(chosen_opt):
            l = unknown[i]
            self.facts[l] = v
            for fact in self.objectivesFacts:
                if fact.fact == l:
                    self.objectivesFacts.remove(fact)
                    self.addNodeCheck(fact)
        return True

    def resolve(self, fact):
        for rule in fact.rules:
            dic = self.getFactUnknown()
            if len(rule.rule[1]) > 1:
                res = self.compute(rule.rule[0], dic)
                if res != None:
                    res2 = self.compute(rule.rule[1], dic)
                    if res2 == None and self.test_all(res, rule.rule, dic) == True:
                        return True
            else:
                # on exécute les rule jusqu'à avoir true
                res = self.compute(rule.rule[0], dic)
                if res == True:
                    self.facts[fact.fact] = True
                    self.objectivesFacts.remove(fact)
                    return True
        return False
  
    def getObjectivesRecursiveRules(self, rules):
        for rule in rules:
            self.getObjectivesRecursiveFacts(rule.firstFacts)
            self.getObjectivesRecursiveFacts(rule.secondFacts)

    def getObjectivesRecursiveFacts(self, facts):
        for fact in facts:
            if fact not in self.nodeChecked and fact not in self.objectivesFacts:
                self.objectivesFacts.append(fact)
                self.getObjectivesRecursiveRules(fact.rules)


"""
    MAIN DE TEST
"""
def main():
    #graph = Graph([['A+B', 'C', '=>'], ['C+D', 'E+A', '=>'], ['E+C', 'A', '=>'], ['D+E', 'B', '=>']], 'CAD', 'E')
    graph = Graph([['A+B', 'C', '=>'], ['D+E', 'A', '=>']], 'CDE', 'C')
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
