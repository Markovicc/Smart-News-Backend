import pandas as pd
import re
from nltk.util import ngrams
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup as bs
from collections import Counter
from nltk.util import bigrams


def key_words(df,stopwords):
    long_tokens = []
    for index,row in df.iterrows():
        tokens = row['uvod'].replace(',',' ').replace('.', ' ').replace('(', ' ').replace(')', ' ').split(' ')
        for t in tokens:
            if len(t)>=4 and t.lower() not in stopwords:
                long_tokens.append(t.capitalize().strip())

    return Counter(long_tokens).most_common(30)
