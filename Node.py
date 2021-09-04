""""""""""""""""""""""""""
#     Dorin Keshales
#       313298424
""""""""""""""""""""""""""


class Node:

    """
    This class represents a Node holding an instance of the GridSearch problem
    Each node contains the problem's state, the leading path, the depth and the total cost of the path so far.
    """

    def __init__(self, state, path, depth, path_cost):
        self.state = state
        self.path = path
        self.depth = depth
        self.path_cost = path_cost

        # Sorted list by action priority, where position 0 which describes right movement is the highest.
        self.prior_action = ["R", "RD", "D", "LD", "L", "LU", "U", "RU"]

    # Get the list of possible actions from current state and return the list of child nodes.
    def expand(self, problem):
        possible_actions = problem.actions(self.state)
        return [self.child_node(problem, action) for action in possible_actions]

    # Create a node for child.
    def child_node(self, problem, action):
        next_state = problem.succ(self.state, action)
        return Node(next_state, self.path + [action], self.depth + 1,
                    self.path_cost + problem.step_cost(self.state, action))

    # Returns a string represents the leading path for this node and this path's cost.
    def solution(self):
        return '{} {}'.format("-".join(self.path), self.path_cost)

    # Returns the priority of the last taken action.
    def action_priority(self):
        return self.prior_action.index(self.path[-1])

    # Representation of node.
    def __repr__(self):
        return f"<{self.state}>"

    # Returns whether the input var is Node type and if it's state equals to the self node's state.
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
