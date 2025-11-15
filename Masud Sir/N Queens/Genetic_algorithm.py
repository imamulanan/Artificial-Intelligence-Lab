import random

# ================== N-Queen Genetic Algorithm ==================

N = 8  # same N (you can change)

def random_chromosome(n):
    # one queen in each column, random row
    return [random.randint(0, n - 1) for _ in range(n)]


# 👉 এখানে দেখা হচ্ছে কোনো দুটি রাণী একে অপরকে আক্রমণ করছে কিনা।
# একই row হলে conflict +1
# একই diagonal হলে conflict +1
def count_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def fitness(state):
    """
    Fitness = number of non-attacking pairs.
    Max pairs = N*(N-1)/2
    Conflicts reduce fitness.
    """
    n = len(state)
    max_pairs = n * (n - 1) / 2
    return max_pairs - count_conflicts(state)

def tournament_selection(population, k=3):
    """
    Pick k random individuals and return the best one.
    """
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: fitness(ind), reverse=True)
    return selected[0]

def crossover(parent1, parent2):
    """
    Single-point crossover.
    """
    n = len(parent1)
    point = random.randint(1, n - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    n = len(chromosome)
    for col in range(n):
        if random.random() < mutation_rate:
            chromosome[col] = random.randint(0, n - 1)
    return chromosome

def genetic_algorithm_n_queens(
    population_size=100,
    generations=1000,
    mutation_rate=0.1
):
    # initial population
    population = [random_chromosome(N) for _ in range(population_size)]

    for gen in range(generations):
        # check if any solution is perfect (no conflicts)
        best = max(population, key=lambda ind: fitness(ind))
        if count_conflicts(best) == 0:
            print(f"Genetic Algorithm: Found solution in generation {gen}")
            return best

        new_population = []

        while len(new_population) < population_size:
            # selection
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            # crossover
            child1, child2 = crossover(parent1, parent2)

            # mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    # return best found if no perfect solution
    print("Genetic Algorithm: No perfect solution found within generation limit.")
    return max(population, key=lambda ind: fitness(ind))

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
solution_ga = genetic_algorithm_n_queens()
print("Final GA state (conflicts =", count_conflicts(solution_ga), "):")
print_board(solution_ga)