# Naive Bayes Classifier (From Scratch)

from collections import defaultdict

class NaiveBayesClassifier:
    def __init__(self):
        self.class_priors = {}
        self.feature_probs = {}
        self.classes = []
    
    # Training function
    def fit(self, X, y):
        """
        X = list of feature vectors (list of lists)
        y = list of class labels
        """
        n_samples = len(X)
        self.classes = set(y)

        # Prior probabilities
        for cls in self.classes:
            self.class_priors[cls] = y.count(cls) / n_samples
        
        # Conditional probabilities
        self.feature_probs = {cls: defaultdict(lambda: 0) for cls in self.classes}
        class_counts = {cls: y.count(cls) for cls in self.classes}
        
        for features, label in zip(X, y):
            for feature in features:
                self.feature_probs[label][feature] += 1
        
        # Normalize probabilities
        for cls in self.classes:
            total = sum(self.feature_probs[cls].values())
            for feature in self.feature_probs[cls]:
                self.feature_probs[cls][feature] /= total
    
    # Prediction for a single instance
    def predict(self, features):
        class_scores = {}
        for cls in self.classes:
            # Start with prior
            score = self.class_priors[cls]
            for feature in features:
                if feature in self.feature_probs[cls]:
                    score *= self.feature_probs[cls][feature]
                else:
                    score *= 1e-6  # smoothing for unseen features
            class_scores[cls] = score
        return max(class_scores, key=class_scores.get)


# ------------------ Example ------------------
X = [
    ["buy", "offer"],      # Spam
    ["cheap", "buy"],      # Spam
    ["hello", "friend"],   # Not Spam
    ["let’s", "meet"],     # Not Spam
]

y = ["Spam", "Spam", "NotSpam", "NotSpam"]

# Train classifier
nb = NaiveBayesClassifier()
nb.fit(X, y)

# Test prediction
test_mail = ["buy", "cheap"]
print("Prediction:", nb.predict(test_mail))
