from tabulate import tabulate

def evaluate(a, b, op):
    if op == "!":   # NOT
        return 1 - a
    if op == "&":   # AND
        return a & b
    if op == "|":   # OR
        return a | b
    if op == "~":   # IMPLIES
        return (not a) | b
    if op == "*":   # IFF (IF AND ONLY IF)
        return int(a == b)

# ডেটা রাখার জন্য লিস্ট
table = []

# Variables = 2 (A, B)
for A in [0, 1]:
    for B in [0, 1]:
        result = evaluate(A, B, "*")
        table.append([A, B, result])

# সুন্দর টেবিল আকারে প্রিন্ট
headers = ["A", "B", "A IFF B"]
print(tabulate(table, headers=headers, tablefmt="grid"))
