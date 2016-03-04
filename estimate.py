# coding: utf-8

# Author: Hussein AL-NATSHEH <hussein.al-natsheh@ish-lyon.cnrs.fr>
# License: BSD 3 clause
# 2016

import argparse
import numpy as np
import pickle

from utils import load_glove

def _define_global(glove_file):
    global glove6b300d
    glove6b300d = load_glove(glove_file, verbose=0)

def _word2glove(word):
    """Get the GloVe vector representation of the word.

    Parameters
    ----------
    :param dframe: Pandas DataFrame
        Pre-trained GloVe loaded dataframe
    
    :param word: string
        word

    Returns
    -------
    :returns: Vecotr
        Glove vector of the word
    """    
    word = word.lower()
    if word not in glove6b300d.index:
        return np.zeros(300, dtype=float, order='C')
    else:
        return np.array(glove6b300d.loc[word])

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

class PairGloveTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        n_samples = len(X)
        Xt = np.zeros(n_samples, dtype=object)
        s_id = 0
        for sample in X:
            lst = []
            for tup in sample:
                w1, w2 = tup
                w1_id, w1_text = w1
                w2_id, w2_text = w2
                w1_vec = _word2glove(w1_text)
                w2_vec = _word2glove(w2_text)
                lst.append(((w1_id, w1_vec), (w2_id, w2_vec)))
            Xt[s_id] = lst
            s_id += 1
        return Xt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--estimator", default='distance_model.pickle', type=str)
    parser.add_argument("--sent1", default='There was a rather ridiculous young man on it— indigo neck, cord round his hat', type=str)
    parser.add_argument("--sent2", default='There was a young man on this bus who was rather ridiculous, not because he wasn’t carrying a bayonet, but because he looked as if he was carrying one when all the time he wasn’t carrying one.', type=str)
    parser.add_argument("--glovefile", default='data/glove.6B.300d.txt', type=str)
    args = parser.parse_args()

    X = np.zeros(shape=(1,2), dtype=object)
    X[0][0] = args.sent1
    X[0][1] = args.sent2

    _define_global(args.glovefile)
    
    estimator = pickle.load(open(args.estimator,"r"))
    sensim = estimator.predict(X)

    print ('Sentence 1: ', args.sent1)
    print ('Sentence 2: ', args.sent2)
    print ('Estimated semantic text similarity', sensim)