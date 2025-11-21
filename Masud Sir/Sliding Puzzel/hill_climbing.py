import random

# We represent the puzzle as a tuple of 9 numbers (0 is the blank)
# Indexes:
# 0 1 2
# 3 4 5
# 6 7 8

# ----------------- HEURISTIC FUNCTION -----------------
def heuristic(state, goal):
    """
    Heuristic: number of misplaced tiles (ignoring the blank 0).
    Lower is better. 0 means goal state.
    """
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

# ----------------- NEIGHBOR GENERATION -----------------
def get_neighbors(state):
    """
    Generate all valid neighbor states by sliding a tile into the blank.
    """
    neighbors = []
    zero_index = state.index(0)  # position of the blank
    row = zero_index // 3
    col = zero_index % 3

    # possible moves: up, down, left, right
    moves = []
    if row > 0:
        moves.append(-3)   # move blank up
    if row < 2:
        moves.append(3)    # move blank down
    if col > 0:
        moves.append(-1)   # move blank left
    if col < 2:
        moves.append(1)    # move blank right

    for move in moves:
        new_index = zero_index + move
        new_state = list(state)
        # swap blank (0) with the tile at new_index
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))

    return neighbors

# ----------------- HILL CLIMBING -----------------
def hill_climbing(initial_state, goal_state, max_steps=1000):
    """
    Steepest-ascent hill climbing:
    - start from initial_state
    - repeatedly move to the neighbor with the lowest heuristic
    - stop if no neighbor is better (local optimum or goal)
    """
    current = initial_state
    current_h = heuristic(current, goal_state)

    for step in range(max_steps):
        if current_h == 0:
            print(f"Reached goal at step {step}!")
            return current

        neighbors = get_neighbors(current)

        # find the neighbor with the lowest heuristic value
        best_neighbor = None
        best_h = float('inf')

        for n in neighbors:
            h = heuristic(n, goal_state)
            if h < best_h:
                best_h = h
                best_neighbor = n

        # if no improvement, stop (local maximum / plateau)
        if best_h >= current_h:
            print("No better neighbor found. Stuck in local optimum.")
            return current

        # move to the best neighbor
        current = best_neighbor
        current_h = best_h

        print(f"Step {step + 1}, heuristic = {current_h}")
        print_state(current)
        print("-" * 20)

    return current

# ----------------- UTILITY: PRINTING -----------------
def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else " " for x in row))

# ----------------- EXAMPLE RUN -----------------
# Example initial and goal states:
#
# Initial (one possible puzzle):
# 1 2 3
# 4 0 6
# 7 5 8
#
# Goal:
# 1 2 3
# 4 5 6
# 7 8 0
#
# Represented as:
# initial_state = (1, 2, 3,
#                  4, 0, 6,
#                  7, 5, 8)
#
# goal_state    = (1, 2, 3,
#                  4, 5, 6,
#                  7, 8, 0)

initial_state = (1, 2, 3,
                 4, 0, 6,
                 7, 5, 8)

goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

print("Initial state:")
print_state(initial_state)
print("==============")

final_state = hill_climbing(initial_state, goal_state)

print("Final state reached:")
print_state(final_state)