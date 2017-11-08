
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


		### On Créer le Graphe
		self.setFacts()
		self.createNodes()
		self.linkRulesAndFacts()
		self.createQuerieGraph()
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


"""
	MAIN DE TEST
"""
def main():
	graph = Graph([['A|B+C', 'E'], ['(F|G)+H', 'E']], 'BC', 'E')

if __name__ == '__main__':
	main()