# neural_net.py  (no numpy version)
import random
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

outlook_vals = ['Sunny', 'Overcast', 'Rain']
temp_vals = ['Hot', 'Mild', 'Cool']


# ------------------------ Encoding ------------------------
def encode_row(row):
    """
    row: [Outlook, Temp, Label]
    Returns:
        x: list of 6 floats (one-hot: 3 for Outlook, 3 for Temp)
        y: float, 1.0 for Yes, 0.0 for No
    """
    outlook, temp, label = row
    x = []

    # One-hot encode Outlook
    for val in outlook_vals:
        x.append(1.0 if outlook == val else 0.0)

    # One-hot encode Temp
    for val in temp_vals:
        x.append(1.0 if temp == val else 0.0)

    y = 1.0 if label == 'Yes' else 0.0
    return x, y


X = []
y = []
for row in dataset:
    xi, yi = encode_row(row)
    X.append(xi)
    y.append(yi)


# ------------------------ Neural Network (1 hidden layer) ------------------------
def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


def init_network(n_inputs, n_hidden):
    # W1: n_inputs x n_hidden
    # b1: n_hidden
    # W2: n_hidden x 1
    # b2: scalar
    rng = random.Random(0)

    W1 = [[rng.uniform(-0.1, 0.1) for _ in range(n_hidden)] for _ in range(n_inputs)]
    b1 = [0.0 for _ in range(n_hidden)]
    W2 = [rng.uniform(-0.1, 0.1) for _ in range(n_hidden)]
    b2 = 0.0

    return W1, b1, W2, b2


def forward(x, W1, b1, W2, b2):
    """
    x: list length n_inputs
    returns:
        a1: list hidden activations
        a2: scalar output
    """
    n_hidden = len(b1)

    # Hidden layer
    z1 = []
    a1 = []
    for j in range(n_hidden):
        s = b1[j]
        for i in range(len(x)):
            s += x[i] * W1[i][j]
        z = s
        z1.append(z)
        a1.append(sigmoid(z))

    # Output layer
    s2 = b2
    for j in range(n_hidden):
        s2 += a1[j] * W2[j]
    z2 = s2
    a2 = sigmoid(z2)

    return a1, a2


def train_network(X, y, n_hidden=4, lr=0.5, epochs=3000):
    n_inputs = len(X[0])
    n_samples = len(X)

    W1, b1, W2, b2 = init_network(n_inputs, n_hidden)

    for epoch in range(epochs):
        loss_sum = 0.0

        # Stochastic gradient descent: update per sample
        for idx in range(n_samples):
            x = X[idx]
            target = y[idx]

            # ---- Forward ----
            a1, a2 = forward(x, W1, b1, W2, b2)

            # Loss: 0.5 * (a2 - target)^2
            error = a2 - target
            loss_sum += error * error

            # ---- Backprop ----
            # dL/da2 = (a2 - y)
            dL_da2 = error
            # da2/dz2 = a2 * (1 - a2)
            da2_dz2 = a2 * (1.0 - a2)
            # dL/dz2
            dL_dz2 = dL_da2 * da2_dz2

            # Gradients for W2 and b2
            dW2 = [dL_dz2 * a1_j for a1_j in a1]
            db2 = dL_dz2

            # Backprop to hidden layer
            dL_da1 = [dL_dz2 * W2_j for W2_j in W2]  # list length n_hidden
            dL_dz1 = []
            for j in range(n_hidden):
                da1_dz1 = a1[j] * (1.0 - a1[j])
                dL_dz1.append(dL_da1[j] * da1_dz1)

            # Gradients for W1 and b1
            dW1 = []
            for i in range(n_inputs):
                row_grad = []
                for j in range(n_hidden):
                    row_grad.append(dL_dz1[j] * x[i])
                dW1.append(row_grad)

            db1_grad = dL_dz1[:]  # copy

            # ---- Gradient descent update ----
            # Update W2, b2
            for j in range(n_hidden):
                W2[j] -= lr * dW2[j]
            b2 -= lr * db2

            # Update W1, b1
            for i in range(n_inputs):
                for j in range(n_hidden):
                    W1[i][j] -= lr * dW1[i][j]
            for j in range(n_hidden):
                b1[j] -= lr * db1_grad[j]

        # Average loss
        avg_loss = loss_sum / n_samples
        if epoch % 500 == 0:
            print(f"Epoch {epoch}, loss = {avg_loss:.4f}")

    return W1, b1, W2, b2


def predict(sample_features, W1, b1, W2, b2):
    """
    sample_features: ['Sunny', 'Cool'] etc.
    Returns: ('Yes'/'No', probability_of_Yes)
    """
    outlook, temp = sample_features
    x = []

    # encode outlook
    for val in outlook_vals:
        x.append(1.0 if outlook == val else 0.0)
    # encode temp
    for val in temp_vals:
        x.append(1.0 if temp == val else 0.0)

    a1, a2 = forward(x, W1, b1, W2, b2)
    prob_yes = a2
    label = 'Yes' if prob_yes >= 0.5 else 'No'
    return label, prob_yes


# ------------------------ Main ------------------------
def main():
    W1, b1, W2, b2 = train_network(X, y, n_hidden=4, lr=0.5, epochs=3000)

    test_samples = [
        ['Sunny', 'Cool'],
        ['Overcast', 'Mild'],
        ['Rain', 'Hot'],
        ['Sunny', 'Hot']
    ]

    print("\n--- Test Predictions ---")
    for sample in test_samples:
        label, prob = predict(sample, W1, b1, W2, b2)
        print(f"Sample: {sample} -> Predicted: {label} (P(Yes) = {prob:.3f})")


if __name__ == "__main__":
    main()