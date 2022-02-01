import pygame
from custom_tools import Geometry, Node
import search
import math

# ******* Custom problem attributes ********

plane_dimensions = (1000, 800)
polygons = [[0.62, 2], [2, 1.5], [2.3, 3.2]], [[4, 4], [4, 2], [12, 2], [12, 4]], [[2.5, 6.75], [2.5, 4.5], [5, 6.6]], [[6, 8], [6, 5], [9,5], [9,8]], [[10,12],[10,5], [12,5], [12,12]], [[13,1], [16,6], [19,1]], [[13,9], [15,6], [16,9]], [[14,12], [14,11], [20,11], [20,12]]
#polygons =  [[14,12], [14,11], [20,11], [20,12]], [[6, 8], [6, 5], [9,5], [9,8]], [[10,20],[10,10], [12,15], [12,20]]

origin_point = [1,1]
destiny_point = [18,13]

# ******************************************

# scale polygons by scalar
scalar = 30
p = 0
for polygon in polygons:
    v = 0
    for vertex in polygon:
        c = 0
        for coord in vertex:
            coord *= scalar
            polygons[p][v][c] = coord
            c += 1
        v += 1
    p += 1

for i in range(0,2):
    origin_point[i] *= scalar
    destiny_point[i] *= scalar



# GRAPH GENERATION

# set nodes
nodes = list()
for polygon in polygons:
    for vertex in polygon:
        nodes.append(Node(vertex[0], vertex[1]))
nodes.append(Node(origin_point[0], origin_point[1]))
nodes.append(Node(destiny_point[0], destiny_point[1]))

# separate poly edges to check intersections between nodes
all_separated_edges = list()
for polygon in polygons:
    for edge in Geometry.get_polygon_edges(polygon):
        all_separated_edges.append(edge)


# set node connections
for node in nodes:
    for other_node in nodes:
        if not node.__eq__(other_node):
            intersects = False
            for edge in all_separated_edges:
                if Geometry.line_intersection((node.get_pos(), other_node.get_pos()), (edge.nodeA.get_pos(), edge.nodeB.get_pos())):
                    intersects = True
            if not intersects:
                node.connect_to(other_node)

# shortest path algorithm
class ExerciseProblem(search.Problem):

        def __init__(self):
            self.initial = tuple(origin_point)
            self.goal = tuple(destiny_point)
            search.Problem.__init__(self, self.initial, self.goal)

        def actions(self, state):
            return [action for action in self.get_node_from_tuple(state).connections]

        @staticmethod
        def get_node_from_tuple(tuple):
            for node in nodes:
                if node.x == tuple[0] and node.y == tuple[1]:
                    return node

        def result(self, state, action):
            return tuple(action.get_pos())

        def h(self, node):
            result = math.sqrt((self.goal[0] - node.state[0])**2 + (self.goal[1] - node.state[1])**2)
            return result

        def path_cost(self, c, state1, action, state2):
            cost = math.sqrt((state2[0] - state1[0])**2 + (state2[1] - state1[1])**2)
            return c + cost

"""
solution = search.depth_first_graph_search(ExerciseProblem())
print('DFS actions: ', solution.solution())
print('DFS path:', solution.path())
print('Final state (DFS): ', solution)
print('')
"""

"""
solution = search.breadth_first_graph_search(ExerciseProblem())
print('BFS: ', solution.solution())
print('Final state (BFS): ', solution)
"""

solution = search.astar_search(ExerciseProblem())
print('A*: ', solution.solution())

"""
solution = search.uniform_cost_search(ExerciseProblem())
print('Uniform cost: ', solution.solution())
"""
# searches comparison
search.compare_searchers([ExerciseProblem()], "Exercise", [search.depth_first_graph_search, search.breadth_first_graph_search, search.astar_search, search.uniform_cost_search])




# graphic representation
BACKGROUND_COLOR = (255, 255, 255)
POLYGON_COLOR = (0, 0, 0)
LINE_COLOR = (0, 255, 0)
POINT_COLOR = (255, 0, 0)
SHORTEST_PATH_COLOR = (0, 0, 255)

pygame.init()
pygame.display.set_caption('Pràctica 1')
screen = pygame.display.set_mode(plane_dimensions)
exit_condition = False

while not exit_condition:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_condition = True

    screen.fill(BACKGROUND_COLOR)

    for node in nodes:
        pygame.draw.circle(screen, POINT_COLOR, [int(node.x), int(node.y)], 5, 1)

    for node in nodes:
        for connection in node.connections:
            pygame.draw.line(screen, LINE_COLOR, (node.x, node.y), (connection.x, connection.y), 1)

    for polygon in polygons:
        pygame.draw.polygon(screen, POLYGON_COLOR, polygon, 1)

    for path_index in range(len(solution.path()) -1):
        from_node = solution.path()[path_index].state
        to_node = solution.path()[path_index + 1].state
        pygame.draw.line(screen, SHORTEST_PATH_COLOR, (from_node[0], from_node[1]), (to_node[0], to_node[1]), 2)

    pygame.display.flip()

pygame.quit()




