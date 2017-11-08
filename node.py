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
		self.objectivesFacts = []

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
				self.objectivesFacts.append(fact)
				self.getObjectivesRecursiveRules(fact.rules)

		# On enlève de la liste des objectif les facts qui n'ont pas de rules
		for fact in self.objectivesFacts:
			if not fact.rules:
				self.objectivesFacts.remove(fact)

		# Maintenant qu'on a la liste il faut résoudre les équations de chaque facts en partant du bas de la liste
		#
		# /!\ MESSAGE : Il faut faire tourner en boucle dans la liste d'objectif pour résoudre les équations et trouvé au moins 1 true
		# En suite si on le trouve on l'enlève de la liste
		#

		while (self.objectivesFacts):
			i = len(self.objectivesFacts) - 1
			while (i >= 0 and self.objectivesFacts):
				if self.resolve(self.objectivesFacts[i]) == 1:
					# On a trouvé un true donc on recommence du début
					i = len(self.objectivesFacts) - 1
				elif i == 0:
					l = len(self.objectivesFacts) - 1
					# Comme on a pas trouvé de solution on supprime le dernier fact de la liste
					self.objectivesFacts.remove(self.objectivesFacts[l])
				else:
					i -= 1

###
### JEAN SOUI ICI
###
	def resolve(self, fact):
		for rule in fact.rules:
			if len(rule.rule[1]) > 1:
				print("Plus d'un facts impliqué il faut faire des vérifications")
			else:
				# on exécute les rule jusqu'à avoir true
				res = self.compute_condition(rule.rule[0])
				if res == 1:
					self.facts[fact.fact] = 1
					self.objectivesFacts.remove(fact)
					return 1
		return 0

###
### FIN JEAN SOUI ICI
###
		
	def getObjectivesRecursiveRules(self, rules):
		for rule in rules:
			self.getObjectivesRecursiveFacts(rule.firstFacts)
			self.getObjectivesRecursiveFacts(rule.secondFacts)

	def getObjectivesRecursiveFacts(self, facts):
		for fact in facts:
			if self.facts[fact.fact] != 1:
				if fact not in self.objectivesFacts:
					self.objectivesFacts.append(fact)
					self.getObjectivesRecursiveRules(fact.rules)

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
		if tmp == cond or (cond != '1' and cond != '2' and cond != '0'):
			exit_m("could not compute the condition '{:s}'".format(bckup))
		return int(cond)


"""
	MAIN DE TEST
"""
def main():
	graph = Graph([['B', 'A'], ['C', 'A']], '', 'A')
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