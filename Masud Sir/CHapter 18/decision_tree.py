# decision_tree.py
import math
from collections import Counter

# ------------------------ Dataset ------------------------
# Each row: [Outlook, Temp, Play]
dataset = [
    ['Sunny', 'Hot', 'No'],
    ['Sunny', 'Hot', 'No'],
    ['Overcast', 'Hot', 'Yes'],
    ['Rain', 'Mild', 'Yes'],
    ['Rain', 'Cool', 'Yes'],
    ['Rain', 'Cool', 'No'],
    ['Overcast', 'Cool', 'Yes'],
    ['Sunny', 'Mild', 'No'],
    ['Sunny', 'Cool', 'Yes'],
    ['Rain', 'Mild', 'Yes'],
    ['Sunny', 'Mild', 'Yes'],
    ['Overcast', 'Mild', 'Yes'],
    ['Overcast', 'Hot', 'Yes'],
    ['Rain', 'Mild', 'No']
]

features = ["Outlook", "Temp"]  # feature names in order


# ------------------------ Helper functions ------------------------
def entropy(labels):
    total = len(labels)
    counts = Counter(labels)
    ent = 0.0
    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent


def information_gain(data, feature_index):
    """
    data: list of rows [f1, f2, ..., label]
    feature_index: index of feature to split on
    """
    base_entropy = entropy([row[-1] for row in data])
    total = len(data)

    # group rows by feature value
    subsets = {}
    for row in data:
        value = row[feature_index]
        subsets.setdefault(value, []).append(row)

    rem = 0.0
    for subset in subsets.values():
        rem += (len(subset) / total) * entropy([r[-1] for r in subset])

    return base_entropy - rem


def majority_label(data):
    labels = [row[-1] for row in data]
    return Counter(labels).most_common(1)[0][0]


def build_tree(data, feature_names):
    """
    Recursively build decision tree.
    Tree format example:
    {
        'Outlook': {
            'Sunny': { 'Temp': { 'Hot': 'No', 'Mild': 'No', 'Cool': 'Yes' } },
            'Overcast': 'Yes',
            'Rain': { 'Temp': { 'Mild': 'Yes', 'Cool': 'Yes' } }
        }
    }
    """
    labels = [row[-1] for row in data]

    # If all labels same -> leaf node
    if len(set(labels)) == 1:
        return labels[0]

    # If no features left -> majority vote
    if not feature_names:
        return majority_label(data)

    # Choose best feature by information gain
    best_gain = -1
    best_idx = None

    for i, feat in enumerate(feature_names):
        g = information_gain(data, i)
        if g > best_gain:
            best_gain = g
            best_idx = i

    if best_gain <= 0:
        return majority_label(data)

    best_feature = feature_names[best_idx]
    tree = {best_feature: {}}

    # Split data by best feature value
    values = set(row[best_idx] for row in data)
    for v in values:
        # subset of rows where feature == v, with that feature removed
        subset = [row[:best_idx] + row[best_idx + 1:] for row in data if row[best_idx] == v]
        remaining_features = feature_names[:best_idx] + feature_names[best_idx + 1:]
        subtree = build_tree(subset, remaining_features)
        tree[best_feature][v] = subtree

    return tree


def predict_tree(sample, tree, feature_names):
    """
    sample: list like ['Sunny', 'Hot'] (no label)
    tree: decision tree dict built by build_tree()
    """
    sample_dict = {feature_names[i]: sample[i] for i in range(len(feature_names))}
    node = tree

    while isinstance(node, dict):
        feature = next(iter(node))         # current feature name
        value = sample_dict.get(feature)   # value in sample

        if value not in node[feature]:
            # unseen feature value
            return None

        node = node[feature][value]

    # node is now a label
    return node


# ------------------------ Main ------------------------
def main():
    tree = build_tree(dataset, features)
    print("Learned decision tree:")
    print(tree)
    print()

    test_samples = [
        ['Sunny', 'Cool'],
        ['Overcast', 'Mild'],
        ['Rain', 'Hot'],
        ['Sunny', 'Hot']
    ]

    for sample in test_samples:
        pred = predict_tree(sample, tree, features)
        print(f"Test Sample: {sample} -> Predicted Class: {pred}")


if __name__ == "__main__":
    main()