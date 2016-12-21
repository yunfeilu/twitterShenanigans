import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('first.dict')
corpus = corpora.MmCorpus('first.mm')
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
corpus_lsi = lsi[corpus_tfidf]
lsi.print_topics(10)
# for doc in corpus_lsi:
#     print (doc)
lsi.save('first.lsi')
