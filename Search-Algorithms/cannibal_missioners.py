import search

class cannibalMissionerProblem(search.Problem):

    """
    Solves the Cannibal - Missioners Problem where 3 + 3 must cross a river with a 2 person boat and where
    cannibals cannot outnumber missioners in any side of the river
    """
    possible_actions = [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]] # all possible actions: carry in the boat [missioner, cannibal]


    def __init__(self):
        self.initial = (3,3,-1) # initial state left side (missioners, cannibals, boat position) boat left = -1, boat right = 1
        search.Problem.__init__(self, self.initial, (0,0,1))

    def actions(self, state):
        """
        Given a state returns all legal actions (there are persons to be moved and cannibals do not outnumber missioners
        """
        return [b for b in self.possible_actions if self.legal(state, b)]

    def legal(self, state, boat):
        new_state = self.result(state, boat)
        return (new_state[0] == 0 or new_state[0] == 3 or new_state[0] == new_state[1]) and (all(e in range(4) for e in new_state[:2]))

    def result(self, state, action):
        """
        Move persons and boat in the correct direction
        """
        result = [state[i] + state[2] * action[i] for i in range(2)]
        result.append(-1 * state[2])
        return tuple(result)

    def h(self, node):
        result = (node.state[0] + node.state[1])/2
        return result

sol = search.depth_first_graph_search(cannibalMissionerProblem())
print('DFS actions: ', sol.solution())
print('DFS path:', sol.path())
print('Final state (DFS): ', sol)
print('')

"""

sol = search.breadth_first_graph_search(cannibalMissionerProblem())
print('BFS: ', sol.solution())
print('Final state (BFS): ', sol)



sol = search.astar_search(cannibalMissionerProblem())
print('A*: ', sol.solution())
"""

search.compare_searchers([cannibalMissionerProblem()], "Cannibal", [search.depth_first_graph_search, search.breadth_first_graph_search,
                                                                 search.iterative_deepening_search, search.astar_search])
                                                                 

