from collections import deque

# Unidirectional Tree
un_tree = {
    'A': ['B', 'E'],
    'B': ['C', 'D', 'A'],
    'C': ['F', 'B'],
    'D': ['B'],
    'E': ['A'],
    'F': ['C']
}

def bidirectional(tree, start, goal):
    # যদি start আর goal একই হয় তাহলে কিছুই লাগবে না
    if start == goal:
        return None, None  

    # দুটি আলাদা visited লিস্ট -> একদিকে start থেকে, অন্যদিকে goal থেকে
    start_visited = []
    goal_visited = []

    # Queue -> BFS এর জন্য 
    start_queue = deque([start])   # start থেকে BFS
    goal_queue = deque([goal])     # goal থেকে BFS

    # যতক্ষণ পর্যন্ত দুই দিকের queue খালি না হয়
    while start_queue and goal_queue:
        # ----- Start থেকে এক ধাপ BFS -----
        start_node = start_queue.popleft()  # queue থেকে প্রথম নোড বের করলাম
        if start_node not in start_visited:  # যদি আগে ভিজিট না করা থাকে
            start_visited.append(start_node)  # ভিজিটেডে রাখলাম

            # তার সব প্রতিবেশী (neighbour) queue তে যোগ করলাম
            for neighbour in tree[start_node]:
                if neighbour not in start_visited:
                    start_queue.append(neighbour)

        # ----- Goal থেকে এক ধাপ BFS -----
        goal_node = goal_queue.popleft()
        if goal_node not in goal_visited:
            goal_visited.append(goal_node)

            for neighbour in tree[goal_node]:
                if neighbour not in goal_visited:
                    goal_queue.append(neighbour)

        # যদি কোনো নোড দুই দিক থেকেই ভিজিটেড হয় -> মানে পথ মিলে গেছে
        if start_node in goal_visited or goal_node in start_visited:
            return start_visited, goal_visited

# ফাংশন কল
print(bidirectional(un_tree, 'A', 'F'))
