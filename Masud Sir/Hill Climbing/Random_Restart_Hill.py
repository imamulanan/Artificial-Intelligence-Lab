import random

def objective_function(x):
    # Same function: f(x) = -x^2 + 10x
    return -x**2 + 10*x

def get_neighbor(x):
    # Generate a random neighbor by a small step
    step = random.uniform(-1, 1)
    return x + step

def first_choice_hill_climbing(steps=1000, tries_per_step=20):
    """
    First-choice hill climbing:
    - At each step, try up to 'tries_per_step' random neighbors.
    - As soon as a better neighbor is found, move there (first choice).
    """

    # Start with a random solution in [0, 10]
    current_solution = random.uniform(0, 10)
    current_value = objective_function(current_solution)

    for step_index in range(steps):
        improved = False

        for _ in range(tries_per_step):
            neighbor = get_neighbor(current_solution)

            # (Optional) keep x inside [0, 10]
            # neighbor = max(0, min(10, neighbor))

            neighbor_value = objective_function(neighbor)

            if neighbor_value > current_value:
                current_solution = neighbor
                current_value = neighbor_value
                improved = True
                break  # first better neighbor -> move and stop checking

        # if no improvement in this step, just try again next step

    return current_solution, current_value


def random_restart_hill_climbing(restarts=10, steps=1000, tries_per_step=20):
    """
    Random-Restart Hill Climbing:
    - Run first-choice hill climbing many times (restarts).
    - Each run starts from a different random position.
    - Return the overall best solution found.
    """

    best_overall_solution = None
    best_overall_value = float('-inf')

    for r in range(restarts):
        solution, value = first_choice_hill_climbing(steps=steps, tries_per_step=tries_per_step)

        # print(f"Restart {r}: x = {solution:.4f}, f(x) = {value:.4f}")  # optional debug

        if value > best_overall_value:
            best_overall_value = value
            best_overall_solution = solution

    return best_overall_solution, best_overall_value


# ---- Example run ----
best_solution, best_value = random_restart_hill_climbing(
    restarts=10,      # how many random restarts
    steps=1000,       # steps per restart
    tries_per_step=20 # neighbor tries per step in first-choice HC
)

print(f"Best solution found (overall): x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")