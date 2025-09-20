# propositions.py
# Easy truth-table printer for a few propositional sentences.

from itertools import product

def truth_table(var_names, expr, title=""):
    """
    var_names : list of variable names (strings) in order
    expr      : function taking booleans in the same order and returning boolean
    title     : optional string describing the proposition
    """
    print("="*len(title) if title else "="*40)
    if title:
        print(title)
    # header
    header = " | ".join(var_names) + " || " + "Result"
    print(header)
    print("-" * len(header))
    # rows
    for values in product([False, True], repeat=len(var_names)):
        result = expr(*values)
        # print True/False as 1/0 to keep table compact
        row = " | ".join("1" if v else "0" for v in values) + " || " + ("1" if result else "0")
        print(row)
    print()

# --- a) "It is raining outside iff it is a cloudy day."
# Propositional variables: R = raining, C = cloudy
# PL: R ↔ C (biconditional)  -> True when R and C are same
truth_table(
    ["R_raining", "C_cloudy"],
    lambda R_raining, C_cloudy: R_raining == C_cloudy,
    title="(a) R ↔ C  — 'Raining iff Cloudy'"
)

# --- b) "If you get a 100 on the final exam, then you can earn an A in the class."
# Variables: S = score100, A = A_in_class
# PL: S → A   (implication) -> equivalent to (not S) or A
truth_table(
    ["S_score100", "A_gradeA"],
    lambda S_score100, A_gradeA: (not S_score100) or A_gradeA,
    title="(b) S → A  — 'If score100 then A'"
)

# --- c) "Take either 2 Advil or 3 Tylenol."
# Interpret as exclusive or (either one or the other, but not both).
# Variables: Adv = take_2_Advil, Tyl = take_3_Tylenol
# PL: Adv ⊕ Tyl  -> True when exactly one is True
truth_table(
    ["Adv_2", "Tyl_3"],
    lambda Adv_2, Tyl_3: (Adv_2 != Tyl_3),
    title="(c) Adv ⊕ Tyl  — 'Either 2 Advil XOR 3 Tylenol'"
)

# --- d) "She studied hard or she is extremely bright."
# Variables: S = studied_hard, B = extremely_bright
# PL: S ∨ B  (inclusive OR)
truth_table(
    ["S_studied", "B_bright"],
    lambda S_studied, B_bright: S_studied or B_bright,
    title="(d) S ∨ B  — 'Studied hard OR Bright (inclusive)'"
)

# --- e) "I am a rock and I am an island."
# Variables: Rock = am_rock, Isl = am_island
# PL: Rock ∧ Isl (conjunction)
truth_table(
    ["Rock", "Island"],
    lambda Rock, Island: Rock and Island,
    title="(e) Rock ∧ Island  — 'I am a rock AND I am an island'"
)
