import random  # Random number generator for initialization and neighbor selection


def objective_function(x):
    # This is the function we want to maximize: f(x) = -x^2 + 10x
    return -x**2 + 10*x

def get_neighbor(x):
    # Generates a neighboring solution by adding a small random value to x
    step = random.uniform(-1, 1)  # Small random step
    return x + step

def hill_climbing(iterations=1000):
    # Start with a random solution in the range [0, 10]
    current_solution = random.uniform(0, 10)
    current_value = objective_function(current_solution)

    # Repeat for a fixed number of iterations
    for i in range(iterations):
        # Generate a neighbor and evaluate its value
        neighbor = get_neighbor(current_solution)
        neighbor_value = objective_function(neighbor)

        # If the neighbor is better, move to it
        if neighbor_value > current_value:
            current_solution = neighbor
            current_value = neighbor_value

    # Return the best solution found
    return current_solution, current_value

best_solution, best_value = hill_climbing()

# Run the hill climbing algorithm and print the result
best_solution, best_value = hill_climbing()
print(f"Best solution found: x = {best_solution:.4f}")
print(f"Best value: f(x) = {best_value:.4f}")
