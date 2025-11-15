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
    - As soon as we find a better neighbor, move there (first choice).
    - If no better neighbor is found in that step, stay where we are.
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
                # First better neighbor found -> move and stop checking others
                current_solution = neighbor
                current_value = neighbor_value
                improved = True
                # If you want to see progress, uncomment:
                # print(f"Step {step_index}: x = {current_solution:.4f}, f(x) = {current_value:.4f}")
                break  # FIRST-CHOICE: stop after first improvement

        # If no improvement found in this step, we just stay and try again next step

    return current_solution, current_value


# ---- Example run ----
best_solution, best_value = first_choice_hill_climbing()
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")