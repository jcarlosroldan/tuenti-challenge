def solve(S, C, D):
	if C < 4:
		return False
	else:
		return _solve(S, C - 4, D, 4)

operations = [(0,8,0), (0,0,2), (2,0,0), (2,2,0)]
def _solve(S, C, D, tot):
	if S+C+D == 0:
		return tot