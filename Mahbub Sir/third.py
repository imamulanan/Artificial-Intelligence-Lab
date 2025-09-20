from collections import deque

def evaluate_expression(a, b, op):
    """
    & = AND
    | = OR
    ! = NOT
    ~ = IMPLIES
    * = IF AND ONLY IF
    """
    if op == '!':
        return 1 - a
    elif op == '&':
        return a & b
    elif op == '|':
        return a | b
    elif op == '~':
        return (not a) | b
    elif op == '*':
        return int(a == b)


def eval_logic(exp, operand_val):
    exp = exp.replace(" ", "").replace(",", "")
    operators = deque()
    operands = deque()
    negative = False

    for ch in exp:
        if ch in ['&', '|', '~', '*']:
            operators.append(ch)
        elif ch == '!':
            negative = True
        else:
            val = operand_val[ch]
            if negative:
                operands.append(evaluate_expression(val, 0, '!'))
                negative = False
            else:
                operands.append(val)

    # Apply operators in FIFO order (no precedence)
    while operators:
        op = operators.popleft()
        a = operands.popleft()
        b = operands.popleft()
        operands.appendleft(evaluate_expression(a, b, op))

    return operands.popleft()


# ============================
# Example usage
# ============================
operand_val = {
    "a": 1,   # a = True
    "b": 0    # b = False
}

result = eval_logic("a | b & !a ~ b", operand_val)
print("Result:", result)
