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

from heapq import heappush, heappop

def ucs(graph, start, goal):
    # 👉 frontier হলো একটা লিস্ট, যেখানে আমরা priority queue এর মতো করে path গুলো রাখবো। এখানে পরে heap ব্যবহার করা হবে।
    frontier = []

     #     👉 প্রথমে start নোডকে frontier এ ঢোকানো হচ্ছে। 0 → path cost (শুরুতে কোন খরচ নাই তাই 0),start → শুরু নোড
    # [start] → এখন পর্যন্ত যাওয়া path লিস্টে শুধু start node আছে
    heappush(frontier, (0, start, [start])) # path_cost, node, [path]

    # 👉 এই dictionary রাখবে কোন নোডে সবচেয়ে কম খরচে পৌঁছানো গেছে।
    # শুরুতে start নোডে পৌঁছানোর খরচ 0 ধরা হয়েছে।

    best_graph = {start: 0}

    while frontier:

        #heap থেকে সবচেয়ে কম খরচের path টা বের করা হচ্ছে। path_cost → ওই path পর্যন্ত মোট খরচ,node → বর্তমান নোড , path_list → এখন পর্যন্ত পুরো path
        path_cost, node, path_list = heappop(frontier)
        if node == goal:
            return path_cost, path_list
        
        #  বর্তমান node এর সাথে যুক্ত সব neighbor (প্রতিবেশী নোড) এবং তার খরচ (neighbor_cost) নেওয়া হচ্ছে।
        for neighbor, neighbor_cost in graph[node]:
            updated_cost = path_cost + neighbor_cost

            #  চেক করা হচ্ছে: যদি neighbor আগে explore না হয়ে থাকে , অথবা আগে যেটা পাওয়া গেছিল তার থেকে এখনকার খরচ কম হয় ,তাহলে আমরা এই নতুন path ব্যবহার করবো।
            if neighbor not in best_graph or updated_cost < best_graph[neighbor]:
                best_graph[neighbor] = updated_cost
                heappush(frontier, (updated_cost, neighbor, path_list + [neighbor]))
    # যদি frontier খালি হয়ে যায় কিন্তু goal পাওয়া না যায়, তাহলে বোঝাবে যে goal এ যাওয়া সম্ভব না। সে ক্ষেত্রে return করবে (None, ∞) অর্থাৎ path নাই আর খরচ অসীম।
    return None, float("inf")

cost, path= ucs(G, "Arad", "Bucharest")
print("Path : ", " -> ".join(path))
print("Cost : ", cost)