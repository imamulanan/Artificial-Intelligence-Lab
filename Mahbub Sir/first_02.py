import itertools
from tabulate import tabulate
from collections import deque

# ------------- Statement Mapping -------------
statements = {
    "s": ("students", "brilliant", False),   
    "a": ("Real CR", "student", True),
    "b": ("Real CR", "lazy", True) 
}

def print_statement(code, neg=False):
    subject, predicate, singular = statements[code]
    if neg:
        if singular:
            return f"{subject} is not {predicate}"
        else:
            return f"{subject} are not {predicate}"
    else:
        if singular:
            return f"{subject} is {predicate}"
        else:
            return f"{subject} are {predicate}"

# ------------- Build Statement (English) -------------
def build_statement(logic):
    logic = logic.replace(" ", "").replace(",", "")
    result_parts = []
    neg, only_sub = False, False

    for ch in logic:
        if ch == "!":  # Negation
            neg = True
        elif ch == "&":
            result_parts.append("and")
        elif ch == "|":
            result_parts.append("or")
        elif ch == "*":
            result_parts.append("if and only if")
        elif ch == "~":
            result_parts.append("implies")
        elif ch == "A":
            result_parts.append("For all")
            only_sub = True
        elif ch == "E":
            result_parts.append("For some")
            only_sub = True
        elif ch in ["(", ")", ","]:
            continue
        else:  # variable like a, b, s
            if only_sub:
                result_parts.append(statements[ch][0] + ",")
                only_sub = False
            elif neg:
                result_parts.append(print_statement(ch, True))
                neg = False
            else:
                result_parts.append(print_statement(ch))

    return " ".join(result_parts) + "."

# ------------- Evaluate Logic Expression -------------
def evaluate_expression(a, b, op):
    if op == "&": return a and b
    if op == "|": return a or b
    if op == "~": return (not a) or b
    if op == "*": return a == b
    if op == "!": return not a
    return None

def eval_logic(exp, operand_val):
    exp = exp.replace(" ", "").replace(",", "")
    operators, operands = deque(), deque()
    negative = False

    for ch in exp:
        if ch in ['&', '|', '~', '*']:
            operators.append(ch)
        elif ch == '!':
            negative = True
        elif ch in ["(", ")"]:
            continue
        else:
            val = operand_val[ch]
            if negative:
                operands.append(evaluate_expression(val, 0, '!'))
                negative = False
            else:
                operands.append(val)

    while operators:
        op = operators.popleft()
        a = operands.popleft()
        b = operands.popleft()
        operands.appendleft(evaluate_expression(a, b, op))

    return operands.popleft()

# ------------- Truth Table Generator -------------
def truth_table(exp, variables):
    headers = variables + [exp]
    rows = []
    for values in itertools.product([0, 1], repeat=len(variables)):
        operand_val = dict(zip(variables, values))
        result = eval_logic(exp, operand_val)
        rows.append(list(values) + [int(result)])
    print(tabulate(rows, headers=headers, tablefmt="grid"))

# ------------- Example Run -------------
logic1 = "A(s) s"
logic2 = "a & !b ~ a"

print("👉 English Form:")
print(build_statement(logic1))
print(build_statement(logic2))

print("\n👉 Truth Table for:", logic2)
truth_table("a&!b~a", ["a", "b"])
