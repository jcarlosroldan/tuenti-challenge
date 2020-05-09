# Tuenti Challenge Edition 8 Level 14
from networkx import Graph
from networkx.algorithms.shortest_paths.weighted import dijkstra_path_length
from numpy import cross, where, array as nparray
from numpy.linalg import norm
from scipy.spatial import Voronoi, voronoi_plot_2d
from traceback import print_exc
import matplotlib.pyplot as plt

PROBLEM_SIZE = "submit"

# -- jam input/output ------------------------------------------------------- #

def parse_quotient(number):
	divisor, dividend = map(int, number.split("/"))
	return divisor / dividend

def parse_problems(lines):
	""" Given a list of lines, parses them and returns a list of problems. """
	res = []
	i = 0
	while i < len(lines):
		N = int(lines[i])
		points = [list(map(int, ln.split())) for ln in lines[i + 1:i + N + 1]]
		i += N + 1
		radius = parse_quotient(lines[i])
		start, end = [list(map(parse_quotient, ln.split(" "))) for ln in lines[i + 1:i + 3]]
		res.append((points, radius, start, end))
		i += 3
	return res

def solve_all():
	""" Process each test case and generate the output file. """
	res = ""
	with open("%s.in" % PROBLEM_SIZE, "r", encoding="utf-8") as fp:
		lines = fp.read().strip().split("\n")[1:]
	problems = parse_problems(lines)
	for case, problem in enumerate(problems, 1):
		print("Solving Case #%s" % case)
		res += "Case #%s: %s\n" % (case, solve(*problem))
	with open("%s.out" % PROBLEM_SIZE, "w", encoding="utf-8") as fp:
		fp.write(res[:-1])

# -- problem specific functions --------------------------------------------- #

def point_distance(p1, p2):
	return norm(p2 - p1)

def line_distance(l1, l2, p3):
	return norm(cross(l2 - l1, l1 - p3)) / point_distance(l1, l2)

def index(array, element):
	for n, elem in enumerate(array):
		if point_distance(elem, element) < 0.001: return n
	print(array)
	print(element)
	exit()

def solve(points, radius, start, end, debug=False):
	vor = Voronoi(points)
	if debug:
		voronoi_plot_2d(vor)
		plt.plot(*start, 'bo')
		plt.plot(*end, 'ro')
		plt.show()
	start = index(vor.vertices, start)
	end = index(vor.vertices, end)
	g = Graph()
	for (p1, p2), (v1, v2) in vor.ridge_dict.items():
		if v1 == -1 or v2 == -1: continue
		p1_dist = line_distance(vor.vertices[v1], vor.vertices[v2], vor.points[p1])
		p2_dist = line_distance(vor.vertices[v1], vor.vertices[v2], vor.points[p2])
		if p1_dist >= radius and p2_dist >= radius:
			g.add_edge(v1, v2, weight=point_distance(vor.vertices[v1], vor.vertices[v2]))
	try:
		return "%.03f" % dijkstra_path_length(g, source=start, target=end)
	except:
		if debug: print_exc()
		return "IMPOSSIBLE"


# -- entrypoint ------------------------------------------------------------- #

if __name__ == "__main__":
	solve_all()