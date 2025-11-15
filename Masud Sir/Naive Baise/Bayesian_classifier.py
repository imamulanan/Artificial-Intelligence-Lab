# naive.py
import math

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

# Feature names (by column index)
features = ["Outlook", "Temp"]


# ------------------------ Training ------------------------
def train_naive_bayes(data):
    """
    Train a simple Naive Bayes classifier on categorical features.
    data: list of [outlook, temp, label]
    Returns:
        - label_counts: how many times each label appears
        - feature_counts: nested dict with counts per feature value per label
    """
    label_counts = {}     # e.g., {'Yes': 9, 'No': 5}
    feature_counts = {}   # e.g., {'Yes': {'Outlook': {...}, 'Temp': {...}}, ...}

    for row in data:
        outlook, temp, label = row

        # Count each label
        label_counts[label] = label_counts.get(label, 0) + 1

        # Initialize sub-dicts if label not seen before
        if label not in feature_counts:
            feature_counts[label] = {"Outlook": {}, "Temp": {}}

        # Count Outlook feature per label
        feature_counts[label]["Outlook"][outlook] = \
            feature_counts[label]["Outlook"].get(outlook, 0) + 1

        # Count Temp feature per label
        feature_counts[label]["Temp"][temp] = \
            feature_counts[label]["Temp"].get(temp, 0) + 1

    return label_counts, feature_counts


# ------------------------ Prediction ------------------------
def predict_naive_bayes(x, label_counts, feature_counts):
    """
    Predict label for a new sample x using Naive Bayes.
    x: list of feature values [Outlook, Temp]
    """
    total_samples = sum(label_counts.values())
    probs = {}

    for label in label_counts:
        # Start with log prior: log P(label)
        probs[label] = math.log(label_counts[label] / total_samples)

        # For each feature (Outlook, Temp)
        for i, feature in enumerate(features):
            value = x[i]

            # Count of feature=value given label
            count = feature_counts[label][feature].get(value, 0)

            # Total count for this label
            total_feature_count = label_counts[label]

            # Number of unique values for this feature under this label
            unique_feature_values = len(feature_counts[label][feature])

            # Laplace smoothing:
            # P(value | label, feature) = (count + 1) / (total_feature_count + unique_values)
            likelihood = (count + 1) / (total_feature_count + unique_feature_values)

            # Add log-likelihood
            probs[label] += math.log(likelihood)

    # Return label with highest posterior probability
    return max(probs, key=probs.get)


# ------------------------ Main / Test ------------------------
def main():
    # Train the model
    label_counts, feature_counts = train_naive_bayes(dataset)

    # Some test samples (no label, only features)
    test_samples = [
        ['Sunny', 'Cool'],
        ['Overcast', 'Mild'],
        ['Rain', 'Hot'],
        ['Sunny', 'Hot']
    ]

    for sample in test_samples:
        prediction = predict_naive_bayes(sample, label_counts, feature_counts)
        print(f"Test Sample: {sample} -> Predicted Class: {prediction}")

    print("\n--- Model Learned Parameters ---")
    print("Label Counts:", label_counts)
    print("Feature Counts:", feature_counts)


if __name__ == "__main__":
    main()