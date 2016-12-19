from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string

tokens = open("tokens.txt",'w')
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
#stemmer = PorterStemmer()

''' I am not using the stemmer right now because the lemmatizer seems to be more appropriate for the task.
Feel free to switch it around. '''

def clean(doc):
    #doc = " ".join(doc)
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #singles = " ".join(stemmer.stem(plural) for plural in punc_free.split())
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

with open('doc.txt','r') as f:
    for line in f:
        tokens.write(clean(line) + '\n')

tokens.close()