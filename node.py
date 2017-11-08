import re
import ope
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
		self.objectifsFacts = []

		### On Créer le Graphe
		self.setFacts()
		self.createNodes()
		self.linkRulesAndFacts()
		self.createQuerieGraph()
		###

		### On éxecute le backwar chaining
		self.backwardChaining()
		###



	# On récupère et initialise les facts
	def setFacts(self):
		# Les facts true dans ini
		for c in self.initial:
			if c not in self.facts:
				self.facts[c] = 1
		# Les facts False dans les rules
		for i, lst in enumerate(self.rules):
			for j, tab in enumerate(lst):
				for c in tab:
					if c.isalpha() and c.isupper() and c not in self.facts:
						self.facts[c] = 0
        # Les facts False dans ask
		for c in self.queries:
			if c not in self.facts:
				self.facts[c] = 0

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

	# On créer le nouveau graph selon les queries
	def createQuerieGraph(self):
		for querie in self.queries:
			for factNode in self.factNodes:
				if factNode.fact is querie:
					self.graph.append(factNode)


	# Permet de réaliser une liste d'objectif selon si un noeud fact est true ou non
	# et tente de résoudre les rules en prenant en compte 
	def backwardChaining(self):
		for fact in self.graph:
			if self.facts[fact.fact] != 1:
				self.objectifsFacts.append(fact)
				self.evaluateAllRules(fact.rules)
		# Maintenant qu'on a la liste il faut résoudre les équations de chaque facts en partant du bas de la liste
		i = len(self.objectifsFacts) - 1
		while (i >= 0):
			for rule in self.objectifsFacts[i].rules:




				### JEAN SOUI ICI
				###

				res = self.compute_condition(rule.rule[0])
				print(res)

				####
				####



			i -= 1
		
	def evaluateAllRules(self, rules):
		for rule in rules:
			self.evaluateAllFacts(rule.firstFacts)
			self.evaluateAllFacts(rule.secondFacts)

	def evaluateAllFacts(self, facts):
		for fact in facts:
			if self.facts[fact.fact] != 1:
				if fact not in self.objectifsFacts:
					self.objectifsFacts.append(fact)
					self.evaluateAllRules(fact.rules)

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


"""
	MAIN DE TEST
"""
def main():
	graph = Graph([['A|B+C', 'E'], ['(F|G)+H', 'E']], 'BC', 'E')

if __name__ == '__main__':
	main()