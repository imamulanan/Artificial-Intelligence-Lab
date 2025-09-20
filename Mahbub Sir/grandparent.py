# relation data structure
relations = {
    "parent": {},      # child -> parent
    "children": {}     # parent -> [children]
}

def add_person(name):
    if name not in relations["parent"]:
        relations["parent"][name] = None
    if name not in relations["children"]:
        relations["children"][name] = []

def set_parent(parent, child):
    # set parent relation
    relations["parent"][child] = parent
    relations["children"][parent].append(child)

def find_grandparent(name):
    parent = relations["parent"].get(name)
    if parent is None:
        return None
    return relations["parent"].get(parent)


# ---------- Example ----------
add_person("John")
add_person("Mary")
add_person("Joe")

set_parent("John", "Mary")   # John → Mary
set_parent("Mary", "Joe")    # Mary → Joe

print("Joe's grandparent is:", find_grandparent("Joe"))
