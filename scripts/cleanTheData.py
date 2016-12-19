from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
new_tweet_file = open('newtweet.txt','w')


def clean(doc):
    #doc = " ".join(doc)
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #singles = " ".join(stemmer.stem(plural) for plural in punc_free.split())
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

with open('tweet.txt') as f:
    for line in f:
        new_line = clean(line)
        new_tweet_file.write(new_line + '\n')


