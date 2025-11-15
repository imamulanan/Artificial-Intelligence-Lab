import random

# ================== N-Queen Hill Climbing ==================

N = 8  # you can change this

def random_state(n):
    # one queen in each column, random row
    return [random.randint(0, n - 1) for _ in range(n)]

def count_conflicts(state):
    """
    Count number of attacking pairs of queens.
    Lower is better. 0 means a valid solution.
    """
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # same row
            if state[i] == state[j]:
                conflicts += 1
            # same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(state):
    """
    Generate all neighbors by moving each queen in its column,
    and return the neighbor with the fewest conflicts.
    """
    n = len(state)
    best_state = state[:]
    best_conflicts = count_conflicts(state)

    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue
            new_state = state[:]
            new_state[col] = row
            c = count_conflicts(new_state)
            if c < best_conflicts:
                best_conflicts = c
                best_state = new_state
    return best_state, best_conflicts

def hill_climbing_n_queens(max_steps=1000):
    current = random_state(N)
    current_conflicts = count_conflicts(current)

    for step in range(max_steps):
        if current_conflicts == 0:
            print(f"Hill climbing: Found solution in {step} steps")
            return current

        neighbor, neighbor_conflicts = get_best_neighbor(current)

        # no improvement -> local optimum
        if neighbor_conflicts >= current_conflicts:
            print("Hill climbing: Stuck in local optimum.")
            return current

        current = neighbor
        current_conflicts = neighbor_conflicts

    return current

def print_board(state):
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += " Q"
            else:
                line += " ."
        print(line)
    print()

# ---- Example run ----
solution = hill_climbing_n_queens()
print("Final state (conflicts =", count_conflicts(solution), "):")
print_board(solution)