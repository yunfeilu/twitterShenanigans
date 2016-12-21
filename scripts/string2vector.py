import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora

with open('ultimate.txt','r') as f:
    documents = f.read().splitlines()
print (len(documents))

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]
dictionary = corpora.Dictionary(texts)
dictionary.save('ultimate.dict')
print (dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('ultimate.mm',corpus)
