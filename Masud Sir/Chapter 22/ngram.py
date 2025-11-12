# ngram.py
#
# Simple N-gram model (unigram, bigram, trigram) for NLP
# Chapter 22 – N-gram

from collections import defaultdict
import random

# ---------------------- Sample Corpus ----------------------
# You can change / extend these sentences as you like.
corpus_sentences = [
    "I love natural language processing",
    "I love machine learning",
    "natural language processing is fun",
    "language models use n grams",
    "n grams are simple models"
]


# ---------------------- Tokenization -----------------------
def tokenize(sentences):
    """
    Convert list of sentences to one list of tokens.
    Adds <s> and </s> to mark start and end of sentence.
    """
    tokens = []
    for sent in sentences:
        words = sent.lower().split()
        tokens.append("<s>")          # start symbol
        tokens.extend(words)
        tokens.append("</s>")         # end symbol
    return tokens


# ---------------------- N-gram Counts ----------------------
def build_ngram_counts(tokens, n):
    """
    Build n-gram counts from token list.
    Returns:
        ngram_counts: dict mapping n-gram tuple -> count
    """
    ngram_counts = defaultdict(int)

    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])
        ngram_counts[ngram] += 1

    return ngram_counts


def build_ngram_probabilities(ngram_counts, prev_counts=None):
    """
    Build probability table:

    - If prev_counts is None:
        Unigram probabilities:
        P(ngram) = count(ngram) / total_ngrams

    - If prev_counts is provided (bigram, trigram, ...):
        Conditional probabilities:
        P(w_n | w_1..w_{n-1}) = count(ngram) / count(prefix)
    """
    probs = {}

    # Unigram case
    if prev_counts is None:
        total = sum(ngram_counts.values())
        for ngram, c in ngram_counts.items():
            probs[ngram] = c / total
    else:
        # Conditional case: bigram, trigram…
        for ngram, c in ngram_counts.items():
            prefix = ngram[:-1]
            prefix_count = prev_counts[prefix]
            probs[ngram] = c / prefix_count

    return probs


# ---------------------- Text Generation --------------------
def generate_text_bigram(bigram_probs, start_word="<s>", max_words=10):
    """
    Generate text using a simple bigram model P(w_i | w_{i-1}).
    bigram_probs: dict mapping (w1, w2) -> probability
    """
    current_word = start_word
    sentence = []

    for _ in range(max_words):
        # Collect all candidate next words for this current_word
        candidates = []
        probs = []
        for (w1, w2), p in bigram_probs.items():
            if w1 == current_word:
                candidates.append(w2)
                probs.append(p)

        if not candidates:
            break

        # Randomly pick next word according to probabilities
        next_word = random.choices(candidates, weights=probs, k=1)[0]

        if next_word == "</s>":
            break

        sentence.append(next_word)
        current_word = next_word

    return " ".join(sentence)


# ---------------------- Main ------------------------------
def main():
    tokens = tokenize(corpus_sentences)

    # ----- Unigram -----
    unigram_counts = build_ngram_counts(tokens, n=1)
    unigram_probs = build_ngram_probabilities(unigram_counts)

    print("=== Unigram counts (first few) ===")
    for i, (ng, c) in enumerate(unigram_counts.items()):
        if i >= 10:
            break
        print(ng, ":", c)
    print()

    # ----- Bigram -----
    bigram_counts = build_ngram_counts(tokens, n=2)
    bigram_probs = build_ngram_probabilities(bigram_counts, unigram_counts)

    print("=== Bigram counts (first few) ===")
    for i, (ng, c) in enumerate(bigram_counts.items()):
        if i >= 10:
            break
        print(ng, ":", c)
    print()

    # ----- Trigram -----
    trigram_counts = build_ngram_counts(tokens, n=3)
    trigram_probs = build_ngram_probabilities(trigram_counts, bigram_counts)

    print("=== Trigram counts (first few) ===")
    for i, (ng, c) in enumerate(trigram_counts.items()):
        if i >= 10:
            break
        print(ng, ":", c)
    print()

    # ----- Simple bigram generation -----
    print("=== Example text generation with bigram model ===")
    for _ in range(3):
        sentence = generate_text_bigram(bigram_probs, start_word="<s>", max_words=10)
        print("Generated:", sentence)


if __name__ == "__main__":
    main()