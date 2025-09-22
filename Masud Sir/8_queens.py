# hill_climb_8queens.py
# Hill-climbing solver for 8-queens.
# Provide initial_state as a list of 8 integers (columns for each row 0..7).
# If target_state is provided, the algorithm will stop if it reaches that configuration.

import random
import copy

def heuristic(state):
    """Number of attacking pairs of queens. Lower is better. 0 is solution."""
    n = len(state)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def best_neighbor(state):
    """Return (best_state, best_h, move_row, move_col) among neighbors by moving each row's queen."""
    n = len(state)
    current_h = heuristic(state)
    best_h = current_h
    best_state = None
    best_move = None

    for row in range(n):
        original_col = state[row]
        for col in range(n):
            if col == original_col:
                continue
            new_state = state.copy()
            new_state[row] = col
            h = heuristic(new_state)
            if h < best_h:
                best_h = h
                best_state = new_state
                best_move = (row, col)
            # if equal heuristics are also useful for sideways moves; but best_neighbor returns strict best (<)
    return best_state, best_h, best_move

def hill_climb(initial_state, max_sideways=100, restarts=10, randomize_on_restart=True, target_state=None):
    """
    Hill climb with sideways moves and random restarts.
    Returns a tuple (solution_state, solution_h, attempts) where attempts is number of restarts used.
    """
    n = len(initial_state)
    attempt = 0
    state = initial_state.copy()
    while attempt <= restarts:
        current = state.copy()
        current_h = heuristic(current)
        sideways_used = 0
        steps = 0

        print(f"\nRestart #{attempt}, starting h = {current_h}, state = {current}")

        # If start already matches target, finish
        if target_state is not None and current == target_state:
            print("Reached target state immediately at restart", attempt)
            return current, current_h, attempt

        while True:
            steps += 1
            # find all neighbors and choose minimum h (allow equal as sideways)
            nbs = []
            curr_h = heuristic(current)
            best_h = curr_h
            for row in range(n):
                original_col = current[row]
                for col in range(n):
                    if col == original_col:
                        continue
                    new = current.copy()
                    new[row] = col
                    h = heuristic(new)
                    nbs.append((h, row, col, new))
                    if h < best_h:
                        best_h = h

            # find neighbors with best_h
            candidates = [nb for nb in nbs if nb[0] == best_h]
            # pick one candidate randomly (stochastic tie-breaking)
            if not candidates:
                break
            h, row, col, new_state = random.choice(candidates)

            # If improvement
            if h < curr_h:
                current = new_state
                sideways_used = 0
            elif h == curr_h:
                # sideways
                if sideways_used < max_sideways:
                    current = new_state
                    sideways_used += 1
                else:
                    # cannot do more sideways moves
                    break
            else:
                # no better or equal neighbor (local maxima) - stop
                break

            # debug print for every step (you can comment out to reduce output)
            print(f" step {steps}: moved row {row} -> col {col}, h = {h}, state = {current}")

            if target_state is not None and current == target_state:
                print("Reached target state during hill climbing.")
                return current, h, attempt

            if h == 0:
                print("Found solution!")
                return current, 0, attempt

        # not solved: restart
        attempt += 1
        if attempt > restarts:
            break
        if randomize_on_restart:
            # random new state
            state = [random.randrange(n) for _ in range(n)]
        else:
            # slightly perturb current
            state = current.copy()
            r = random.randrange(n)
            state[r] = random.randrange(n)

    return None, heuristic(state), attempt

def print_board(state):
    n = len(state)
    board = []
    for r in range(n):
        row = []
        for c in range(n):
            row.append('Q' if state[r] == c else '.')
        board.append(' '.join(row))
    print('\n'.join(board))

if __name__ == "__main__":
    # === IMPORTANT ===
    # Set initial_state to the configuration from Fig.2.1 (row 0 = topmost row).
    # Example indexing: row 0..7, column 0..7
    # If you don't know the exact positions from the picture, try a random start or paste the list
    # from the figure here.
    #
    # Example (this is a random start; replace with the Fig.2.1 mapping if you want):
    initial_state = [0, 7, 4, 6, 2, 5, 1, 3]  # <-- replace with the initial state's list if you have it
    # Example target if you want the hill-climber to stop when it reaches Fig.2.2:
    target_state = None
    # target_state = [0, 4, 7, 5, 2, 6, 1, 3]  # <-- example solution; replace with Fig.2.2 mapping to check

    print("Initial board (h = {}):".format(heuristic(initial_state)))
    print_board(initial_state)

    solution, sol_h, attempts = hill_climb(
        initial_state=initial_state,
        max_sideways=50,
        restarts=20,
        randomize_on_restart=True,
        target_state=target_state
    )

    if solution:
        print("\nSolution found after restarts used =", attempts)
        print("Heuristic =", sol_h)
        print_board(solution)
    else:
        print("\nNo exact solution found. Best found heuristic:", sol_h)
        if solution is not None:
            print_board(solution)
