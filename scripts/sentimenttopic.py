import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, similarities
import st_model
corpus = corpora.MmCorpus('first.mm')
dictionary = corpora.Dictionary.load('first.dict')
author2doc = {}
sentiment_label = open('sentimentlabel.txt','r')
doc_num = 0
for line in sentiment_label:
    if line not in author2doc:
        author2doc[line] = [doc_num]
    else:
        author2doc[line].append(doc_num)
    doc_num += 1
st = st_model.AuthorTopicModel(corpus,num_topics=20, author2doc=author2doc)
st.print_topics(10)