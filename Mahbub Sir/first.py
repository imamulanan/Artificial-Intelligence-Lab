# শুধু statements map করে রাখবো
statements = {
    "s": ("students", "brilliant", False),   # (subject, predicate, singular?)
    "a": ("Real CR", "student", True),
    "b": ("Real CR", "lazy", True) # subject="Real CR", predicate="student", singular=True
}

def print_statement(code, neg=False):
    subject, predicate, singular = statements[code]
    if neg:
        if singular:
            print(subject, "is not", predicate, end="")
        else:
            print(subject, "are not", predicate, end="")
    else:
        if singular:
            print(subject, "is", predicate, end="")
        else:
            print(subject, "are", predicate, end="")

def build_statement(logic):
    # ইনপুট থেকে space আর comma মুছে ফেলে, যাতে সহজে parse করা যায়।
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
            print("For all ", end="")
            # only_sub=True মানে এর পরে শুধু subject প্রিন্ট করতে হবে (predicate নয়)।
            only_sub = True
        elif ch == "E":
            print("For some ", end="")
            only_sub = True

            # Brackets / comma বাদ দেওয়া
        elif ch in ["(", ")", ","]:
            continue
        else:
            if only_sub:
                print(statements[ch][0], end=", ")
                only_sub = False
            elif neg:
                print_statement(ch, neg=True)
                neg = False
            else:
                print_statement(ch)
                # 👉 তিনটা case:

                # Quantifier পরে থাকলে → শুধু subject দেখাবে।
                # উদাহরণ: A(s) s → "For all students, students are brilliant."

                # neg=True থাকলে → negative statement বানাবে।
                # উদাহরণ: !b → "Real CR is not lazy"

                # normal case → positive statement বানাবে।

    print(".")

# Example Run
build_statement("A(s) s")
build_statement("a & !b ~ a")


# -------------------
# Truth Table Drawing
# -------------------
# def draw_table(li, *args):
#     length = len(" | ".join(args))   # হেডারের দৈর্ঘ্য বের করছে
#     print("-" * length)              # উপরে ড্যাশ লাইন
#     print(" | ".join(args))          # হেডার প্রিন্ট (যেমন: A | B | A AND B)
#     print("-" * length)              # আবার ড্যাশ লাইন
#     for row in li:                   # প্রতিটা রো ঘুরে ঘুরে
#         print(" | ".join(str(i) for i in row))   # রো এর ভ্যালু প্রিন্ট
#     print("-" * length)              # নিচে ড্যাশ লাইন


# draw_table([["1", "1", "1"],
#             ["1", "0", "0"],
#             ["0", "1", "0"],
#             ["0", "0", "0"]], "A", "B", "A AND B")

from tabulate import tabulate  # pip install tabulate

data = [
    ["1", "1", "1"],
    ["1", "0", "0"],
    ["0", "1", "0"],
    ["0", "0", "0"]
]

headers = ["A", "B", "A AND B"]

print(tabulate(data, headers=headers, tablefmt="grid"))









# class Statement:
#     def __init__(self, subject, predicate, singular=True):
#         self.subject = subject
#         self.predicate = predicate
#         self.singular = singular


# class Relation:
#     def __init__(self):
#         self.map = {}

#     def add(self, statement, subject, predicate, singular=True):
#         self.map[statement] = Statement(subject, predicate, singular)

#     def print_statement(self, statement):
#         if self.map[statement].singular:
#             print(self.map[statement].subject, " is ", self.map[statement].predicate, end="")
#         else:
#             print(self.map[statement].subject, " are ", self.map[statement].predicate, end="")

#     def print_neg_statement(self, statement):
#         if self.map[statement].singular:
#             print(self.map[statement].subject, " is not ", self.map[statement].predicate, end="")
#         else:
#             print(self.map[statement].subject, " are not ", self.map[statement].predicate, end="")

#     def build_statement(self, logic):
#         """
#         & = AND
#         | = OR
#         ! = NOT
#         ~ = IMPLIES
#         * = IF AND ONLY IF

#         A = EVERY
#         E = SOME
#         """
#         logic = logic.replace(" ", "")  # no space
#         logic = logic.replace(",", "")  # no comma

#         neg = False
#         only_sub = False

#         for i in range(len(logic)):
#             if logic[i] == '!':
#                 neg = True
#             elif logic[i] == '&':
#                 print(" and ", end="")
#             elif logic[i] == '|':
#                 print(" or ", end="")
#             elif logic[i] == '*':
#                 print(" if and only if, ", end="")
#             elif logic[i] == '~':
#                 print(" implies, ", end="")
#             elif logic[i] == 'A':
#                 print(" For all ", end="")
#                 only_sub = True
#             elif logic[i] == 'E':
#                 print(" For some ", end="")
#                 only_sub = True
#             elif logic[i] in ['(', ')', ',']:
#                 continue
#             else:
#                 if only_sub:
#                     print(self.map[logic[i]].subject, end=", ")
#                     only_sub = False
#                 elif neg:
#                     self.print_neg_statement(logic[i])
#                     neg = False
#                 else:
#                     self.print_statement(logic[i])
#         print(".")

# relation = Relation()

# relation.add("s", "students", "brilliant", singular=False)
# relation.add("a", "Real CR", "student")
# relation.add("b", "Real CR", "lazy")

# relation.build_statement("A(s) s")
# relation.build_statement("a & !b ~ a")

# def draw_table(li, *args):
#     length = len(" | ".join(args))
#     print("-" * length)
#     print(" | ".join(args))
#     print("-" * length)
#     for row in li:
#         print(" | ".join(str(i) for i in row))
#         # print(" | ".join(row))
#     print("-" * length)

# draw_table([["1", "1", "1"], 
#             ["1", "0", "0"], 
#             ["0", "1", "0"], 
#             ["0", "0", "0"]], "A", "B", "A AND B")