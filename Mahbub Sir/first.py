statements = {
    "s": {"subject": "students", "predicate": "brilliant", "singular": False},
    "a": {"subject": "Real CR", "predicate": "student", "singular": True},
    "b": {"subject": "Real CR", "predicate": "brilliant", "singular": True},
}


def print_statement(key):
    st = statements[key]
    if st["singular"]:
        print(f"{st['subject']} is {st['predicate']}", end="")
    else:
        print(f"{st['subject']} are {st['predicate']}", end="")


def print_neg_statement(key):
    st = statements[key]
    if st["singular"]:
        print(f"{st['subject']} is not {st['predicate']}", end="")
    else:
        print(f"{st['subject']} are not {st['predicate']}", end="")


def build_statement(logic):
    logic = logic.replace(" ", "").replace(",", "")
    neg = False
    only_sub = False

    for ch in logic:
        if ch == "!":
            neg = True
        elif ch == "&":
            print(" and ", end="")
        elif ch == "|":
            print(" or ", end="")
        elif ch == "*":
            print(" if and only if, ", end="")
        elif ch == "~":
            print(" implies, ", end="")
        elif ch == "A":
            print(" For all ", end="")
            only_sub = True
        elif ch == "E":
            print(" For some ", end="")
            only_sub = True
        elif ch in ["(", ")"]:
            continue
        else:  # s, a, b ...
            if only_sub:
                print(statements[ch]["subject"], end=", ")
                only_sub = False
            elif neg:
                print_neg_statement(ch)
                neg = False
            else:
                print_statement(ch)
    print(".")

from sympy import symbols
from sympy.logic.boolalg import And, Not, Implies, truth_table
build_statement("A(s) s")
s1, s2, s3 = symbols('s1 s2 s3')
expr = And(s1, s2, s3) # expr = s1 ∧ s2 ∧ s3
print("First Order Logic Expression:")
print("s1 s2 s3 | A(s) s")
for row in truth_table(expr, [s1, s2, s3]):
    vals, value = row # vals = (s1, s2, s3), value = expr
    print(vals[0], vals[1], vals[2], "|", int(bool(value)))



build_statement("a & !b ~ a")

a, b = symbols('a b')
expr = Implies(And(a, Not(b)), a)
print("Propositional Logic Expression:")
print("a b | (a & !b) → a")
for row in truth_table(expr, [a, b]):
    vals, value = row   
    print(vals[0], vals[1], "|", int(bool(value)))
