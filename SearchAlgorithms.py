from PriorityQueue import PriorityQueue
from Node import Node

NO_PATH = "no path"
MAX_DEPTH = 20


# Implementation of Best First Search (BFS) algorithm as part of UCS and A* algorithms.
def best_first_search(problem, f):

    # Create a node with the start state.
    node = Node(problem.start_state, [], 0, 0)

    # Define priority queue with priority function f.
    frontier = PriorityQueue(f)

    expanded_nodes = 0
    frontier.push(node, expanded_nodes, 0)

    closed_list = set()

    # As long the frontier is not empty.
    while frontier.heap:

        node = frontier.pop()

        # If we got to goal.
        if problem.is_goal(node.state):
            return node.solution() + " " + str(expanded_nodes)

        expanded_nodes += 1

        closed_list.add(node.state)

        # For each child of the current node.
        for child in node.expand(problem):

            if child.state not in closed_list and child not in frontier:
                frontier.push(child, expanded_nodes, child.action_priority())

            elif child in frontier and f(child) < frontier[child]:
                del frontier[child]
                frontier.push(child, expanded_nodes, child.action_priority())

    # If no solution was found.
    return NO_PATH


# Implementation of Uniform Cost Search (UCS) algorithm.
def uniform_cost_search(problem):

    def g(node):  # g cost function - returns the cost of the path leading to node.
        return node.path_cost

    return best_first_search(problem, f=g)  # f = g


def a_star(problem):

    def g(node):  # g cost function - returns the cost of the path leading to node.
        return node.path_cost

    def h(node):  # Heuristic function, based on Diagonal distance.

        D, D2 = 1, 1  # When D = 1 and D2 = 1, this is called the Chebyshev distance,

        goal_s = problem.goal_state

        # Calculate the difference between the x coordinates and the y coordinates.
        dx = abs(node.state[0] - goal_s[0])
        dy = abs(node.state[1] - goal_s[1])

        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    return best_first_search(problem, f=lambda n: g(n) + h(n))


# Implementation of Depth Limited Search (dfs-l) algorithm as part of IDS algorithm.
def depth_limited_search(problem, limit):

    # Create a node with the start state.
    node = Node(problem.start_state, [], 0, 0)

    # Here the frontier is a stack data structure.
    frontier = [node]

    expanded_nodes = 0

    # As long the frontier is not empty.
    while frontier:

        node = frontier.pop()

        # If we got to the goal.
        if problem.is_goal(node.state):
            return node.solution(), expanded_nodes

        expanded_nodes += 1

        # If node's depth is under the depth limit.
        if node.depth < limit:
            frontier.extend(node.expand(problem)[::-1])

    return None, expanded_nodes


# Implementation of Iterative Deepening Search (IDS) algorithm.
def iterative_deepening_search(problem):

    total_expanded_nodes = 0

    # Limit to depth up to 20.
    for depth in range(MAX_DEPTH):

        result, expanded_nodes = depth_limited_search(problem, depth)
        total_expanded_nodes += expanded_nodes

        if result:  # If we found a solution
            return "{} {}".format(result, total_expanded_nodes)

    # If no solution was found.
    return NO_PATH


# Implementation of Iterative Deepening A* (IDA*) algorithm.
def iterative_deepening_a_star(problem):

    def g(node):  # g cost function - returns the cost of the path leading to node.
        return node.path_cost

    def h(node):  # Heuristic function, based on Diagonal distance.

        D, D2 = 1, 1  # When D = 1 and D2 = 1, this is called the Chebyshev distance,

        goal_s = problem.goal_state

        # Calculate the difference between the x coordinates and the y coordinates.
        dx = abs(node.state[0] - goal_s[0])
        dy = abs(node.state[1] - goal_s[1])

        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    # Performing DFS according to f, as part of the Iterative Deepening A* (IDA*) algorithm.
    def dfs_f(node, _g, f_limit):

        nonlocal new_limit
        nonlocal expanded_nodes

        new_f = _g + h(node)

        if new_f > f_limit:
            new_limit = min(new_limit, new_f)
            return None

        # If we got to goal.
        if problem.is_goal(node.state):
            return node.solution()

        expanded_nodes += 1

        # Limit to depth up to 20.
        if node.depth < MAX_DEPTH:

            # For each of the node childs.
            for c in node.expand(problem):

                sol = dfs_f(c, g(c), f_limit)

                if sol:  # If not none.
                    return sol

        return None

    # Create a node with the start state.
    start_node = Node(problem.start_state, [], 0, 0)

    f_limit = 0
    expanded_nodes = 0

    new_limit = h(start_node)

    if new_limit == 0:  # If the goal state is also the start state.
        return "{} {}".format(start_node.solution(), expanded_nodes)

    # Loop while resources are available.
    while f_limit != new_limit:

        f_limit = new_limit
        new_limit = float('inf')

        solution = dfs_f(start_node, 0, f_limit)

        if solution:  # If solution was found
            return "{} {}".format(solution, expanded_nodes)

    # If no solution was found.
    return NO_PATH
