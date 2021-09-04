from SearchAlgorithms import iterative_deepening_search, uniform_cost_search, a_star, iterative_deepening_a_star

""""""""""""""""""""""""""
#     Dorin Keshales
#       313298424
""""""""""""""""""""""""""

INPUT_FILE = "./input.txt"
OUTPUT_FILE = "./output.txt"


class GridSearch:

    """
    This class is a representation of the Grid Search problem.
    An instance of this class will contain the input grid, the start state, the goal state, the grid size, the possible
    moves that can be made on the grid and helper functions returning possible actions from current state, cost of
    performing an action from the current state, successors of current state and if whether we reached goal state.
    """

    def __init__(self, grid, start, goal, n):
        self.grid = grid
        self.start_state = start
        self.goal_state = goal
        self.grid_size = n

        self.moves = {  # The conditions that must be met for any action to be taken.

            # Right
            'R': lambda x: x[1] < grid_size - 1 and self.grid[x[0]][x[1] + 1] != -1,

            # Right Down
            'RD': lambda x: x[1] < grid_size - 1 and x[0] < grid_size - 1 and self.grid[x[0] + 1][x[1] + 1] != -1 and
                            self.grid[x[0]][x[1] + 1] != -1 and self.grid[x[0] + 1][x[1]] != -1,

            # Down
            'D': lambda x: x[0] < grid_size - 1 and self.grid[x[0] + 1][x[1]] != -1,

            # Left Down
            'LD': lambda x: x[1] > 0 and x[0] < grid_size - 1 and self.grid[x[0] + 1][x[1] - 1] != -1 and
                            self.grid[x[0]][x[1] - 1] != -1 and self.grid[x[0] + 1][x[1]] != -1,

            # Left
            'L': lambda x: x[1] > 0 and self.grid[x[0]][x[1] - 1] != -1,

            # Left Up
            'LU': lambda x: x[1] > 0 and x[0] > 0 and self.grid[x[0] - 1][x[1] - 1] != -1 and self.grid[x[0]][
                x[1] - 1] != -1 and self.grid[x[0] - 1][x[1]] != -1,

            # Up
            'U': lambda x: x[0] > 0 and self.grid[x[0] - 1][x[1]] != -1,

            # Right Up
            'RU': lambda x: x[1] < grid_size - 1 and x[0] > 0 and self.grid[x[0] - 1][x[1] + 1] != -1 and
                            self.grid[x[0]][x[1] + 1] != -1 and self.grid[x[0] - 1][x[1]] != -1
        }

        self.transitions = {'R': (0, 1), 'RD': (1, 1), 'D': (1, 0), 'LD': (1, -1), 'L': (0, -1), 'LU': (-1, -1),
                            'U': (-1, 0), 'RU': (-1, 1)}

    # Returns the possible moves from current state.
    def actions(self, state):
        return [m for (m, f) in self.moves.items() if f(state)]

    # Returns the new state obtained by activating the action on the current state.
    def succ(self, state, action):
        return tuple(map(sum, zip(state, self.transitions[action])))

    # Returns the cost of performing the action from the current state.
    def step_cost(self, state, action):
        new_state = self.succ(state, action)
        return self.grid[new_state[0]][new_state[1]]

    # Returns if the received state is the goal state.
    def is_goal(self, state):
        return self.goal_state == state


def read_input_file():

    # Read the input data.
    with open(INPUT_FILE, "r", encoding="utf-8") as input_file:
        data = input_file.readlines()

    # Extract the algorithm name, start position, end position and grid size from the first 4 lines in the file.
    algo = data[0].strip().split()[0]
    start = tuple(int(item) for item in data[1].strip().split(','))
    end = tuple(int(item) for item in data[2].strip().split(','))
    n = int(data[3].strip())

    grid = []

    # Finally, extract the grid itself (I'm counting on valid input as declared).
    for line in data[4:]:
        grid.append([int(item) for item in line.rstrip('\n').split(',')])

    return algo, start, end, n, grid


if __name__ == "__main__":

    # Extract the relevant information from the input file.
    algorithm, start_pos, end_pos, grid_size, grid = read_input_file()

    # Create an instance of GridSearch.
    problem = GridSearch(grid, start_pos, end_pos, grid_size)

    # Find solution using the selected algorithm.
    if algorithm == "IDS":
        solution = iterative_deepening_search(problem)

    elif algorithm == "UCS":
        solution = uniform_cost_search(problem)

    elif algorithm == "ASTAR":
        solution = a_star(problem)

    elif algorithm == "IDASTAR":
        solution = iterative_deepening_a_star(problem)

    else:
        raise ValueError("Algorithm is not supported.")

    # Write the solution to the output file.
    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(solution)
