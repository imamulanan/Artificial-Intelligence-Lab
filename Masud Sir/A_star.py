# Undirected weighted graph: city -> list of (neighbor, distance_km)
G = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)],
}

# Straight-line distances to Bucharest (heuristic)
H = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242, "Eforie": 161,
    "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151, "Iasi": 226, "Lugoj": 244,
    "Mehadia": 241, "Neamt": 234, "Oradea": 380, "Pitesti": 100,
    "Rimnicu Vilcea": 193, "Sibiu": 253, "Timisoara": 329, "Urziceni": 80,
    "Vaslui": 199, "Zerind": 374,
}

from heapq import heappush, heappop

def a_star(graph, heuristic, start, goal):
    # Priority Queue -> (f, g, node, path)
    frontier = []
    heappush(frontier, (heuristic[start], 0, start, [start]))

    # best_graph[node] = সর্বনিম্ন g-value (actual cost) to reach node
    best_graph = {start: 0}

    while frontier:
        # g(n) মানে হলো start থেকে এখন পর্যন্ত সেই নোডে পৌঁছানোর আসল খরচ।
        # h(n) মানে হলো নোড n থেকে goal (Bucharest) পর্যন্ত আনুমানিক খরচ।
        # f(n) = g(n) + h(n)
        f, g, node, path = heappop(frontier) 

        # Goal check
        if node == goal:
            return g, path

        # Explore neighbors
        for neighbor, cost in graph[node]:
            g_new = g + cost              # নতুন actual cost
            f_new = g_new + heuristic[neighbor]  # f = g + h

            if neighbor not in best_graph or g_new < best_graph[neighbor]:
                best_graph[neighbor] = g_new
                heappush(frontier, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float("inf")  # যদি goal এ পৌঁছানো না যায়

# Run A*
cost, path = a_star(G, H, "Arad", "Bucharest")
print("Path :", " -> ".join(path))
print("Cost :", cost)
