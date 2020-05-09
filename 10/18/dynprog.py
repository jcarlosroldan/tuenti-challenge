# -- the dynamic programming snippet -------------------------------------------

class DynProg:
	""" Abstract class to solve problems using dynamic programming. To use it,
	make a child class implementing alternatives, is_final and penalty. Then,
	make one of such objects providing the initial state in the constructor, and
	call to solve(), providing one search type. """
	ONE_SOLUTION = 0
	ONE_OPTIMAL_SOLUTION = 1
	ALL_SOLUTIONS = 2
	ALL_OPTIMAL_SOLUTIONS = 3

	def __init__(self, initial_state):
		self.initial_state = initial_state

	def alternatives(self, state):
		raise NotImplementedError("This should return all the alternatives for a given state, without modifying the given state.")

	def is_final(self, state):
		raise NotImplementedError("This should return whether a state is a final state or not.")

	def penalty(self, state):
		raise NotImplementedError("This should return an upper bound for the penalty of the problem. Ideally, optimal solutions should have no penalty.")

	def solve(self, search_type=ONE_SOLUTION):
		assert search_type in range(4), "Invalid search type."
		final_states = []
		explored = []
		remaining = [(self.penalty(self.initial_state), self.initial_state)]
		if self.is_final(self.initial_state):
			if search_type == self.ONE_OPTIMAL_SOLUTION:
				return self.initial_state
			else:
				final_states.append((self.penalty(self.initial_state), self.initial_state))
		while len(remaining):
			_, state = remaining.pop(0)
			explored.append(state)
			for alternative in self.alternatives(state):
				if alternative in explored: continue
				penalty = self.penalty(alternative)
				if self.is_final(alternative):
					if search_type == self.ONE_SOLUTION or penalty == 0 and search_type == self.ONE_OPTIMAL_SOLUTION:
						return alternative
					else:
						final_states.append((penalty, alternative))
				else:
					index = sum(1 for p, _ in remaining if p < penalty)
					remaining.insert(index, (penalty, alternative))
		if search_type == self.ALL_SOLUTIONS:
			return [state for _, state in final_states]
		else:
			min_penalty = min([penalty for penalty, _ in final_states])
			optimals = [state for penalty, state in final_states if penalty == min_penalty]
			if search_type == self.ALL_OPTIMAL_SOLUTIONS:
				return optimals
			else:
				return optimals[0]

# -- the usage example ---------------------------------------------------------

class NQueens(DynProg):
	""" Simple child class to give an example of use. Solves N-Queens problems
	using dynamic programming. """
	def __init__(self, N):
		self.N = N
		self.initial_state = []

	def alternatives(self, state):
		res = []
		col = len(state)
		for row in range(self.N):
			if row in state:
				continue
			diag1 = row - col
			diag2 = row + col
			if any(r - c == diag1 for c, r in enumerate(state)) or any(r + c == diag2 for c, r in enumerate(state)):
				continue
			res.append(state + [row])
		return res

	def is_final(self, state):
		return len(state) == self.N

	def penalty(self, state):
		return len(self.alternatives(state))

if __name__ == "__main__":
	nq = NQueens(10)
	print(len(nq.solve(NQueens.ALL_SOLUTIONS)))