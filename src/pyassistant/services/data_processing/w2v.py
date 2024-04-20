from collections import Counter
from typing import List

import gensim
import gensim.downloader
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

STOP_WORDS = set(nltk.corpus.stopwords.words('english'))

def load_w2v() -> gensim.models.Word2Vec:
    """Load (download if necessary) the Word2Vec model.

    Returns:
        gensim.models.Word2Vec: w2v model.
    """
    return gensim.downloader.load('word2vec-google-news-300')


model = load_w2v()


def tokenize(sentence: str) -> List[str]:
    """Tokenize sentence and remove stop words.

    Args:
        sentence (str): Sentence to tokenize.

    Returns:
        List[str]: List with tokens.
    """
    tokens = [t.lower() for t in nltk.word_tokenize(sentence)]
    return [t for t in tokens if t not in STOP_WORDS]


def vectorize_phrase(sentence: str, model: gensim.models.Word2Vec=None) -> np.array:
    """Vectorize a phrase by first tokenizing it, apply the vectorization
    using `model` and then averaging the vector over all tokens excluding stopwords.

    Args:
        sentence (str): Sentence to vectorize.
        model (_type_, optional): Word embedding Model. Defaults to None.

    Returns:
        np.array: Vector embedding for the sentence.
    """
    tokens = tokenize(sentence)
    if not tokens:
        return 0
    token_count = Counter(tokens)
    weights = [token_count[token] for token in token_count if token in model]
    if not weights:
        return None
    return np.average([model[token] for token in token_count if token in model], axis=0, weights=weights).reshape(1, -1)


def compare_vectors(sentence_vec: np.array, reference_vecs: List[np.array]):
    comp_scores = [cosine_similarity(sentence_vec.reshape(1, -1), ref_vec.reshape(1, -1))[0][0] for ref_vec in reference_vecs]
    return max(comp_scores), sum(comp_scores) / len(comp_scores)


def compare_strings(word: str, reference_words: List[str], certainty: int=80) -> str:
    word = word.lower()
    for ref in reference_words:
        if fuzz.partial_ratio(word, ref.lower()) > certainty:
            return word
    return None
