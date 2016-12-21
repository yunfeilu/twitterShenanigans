import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('ultimate.dict')
corpus = corpora.MmCorpus('ultimate.mm')
print (corpus)
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=20)
lda.print_topics(20)

