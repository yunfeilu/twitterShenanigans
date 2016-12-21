from __future__ import print_function

import numpy as np
from scipy.special import gammaln
import time

from six.moves import xrange

from .base import BaseGibbsParamTopicModel
from .formatted_logger import formatted_logger

logger = formatted_logger('sentimentTopicModel', 'info')
class SentimentTopicMode(BaseGibbsPramTopicModel):
    def __init__(self, n_doc, n_voca, n_topic, n_sentiments = 3, alpha=0.1, beta=0.01, **kwargs):
        super(SentimentTopicMode, self).__init__(n_doc, n_voca, n_topic, alpha, beta, **kwargs)
        self.n_sentiments = n_sentiments

        self.ST = np.zeros([self.n_sentiments, self.n_topic]) + self.alpha
        self.topic_assigned = list()
        self.sentiment_assigned = list()
        self.sum_S = np.zeros(self.n_sentiments) + self.alpha * self.n_sentiments

    def fit(self, docs, doc_sentiments, max_iter=100):
        if type(docs[0][0]) != int:
            _docs = list()
            for doc in docs:
                _doc = list()
                for word in doc:
                    doc.append(int(word))
                _docs.append(doc)
            docs = _docs

        if type(doc_sentiments[0][0]) != int:
            _doc_sentiments = list()
            for doc in doc_sentiments:
                _doc = list()
                for sentiment in doc:
                    _doc.append(int(sentiment))
                _doc_sentiments.append(_doc)
            doc_sentiments = _doc_sentiments

        self.random_init(docs, doc_sentiments)
        self.gibbs_sampling(docs, doc_sentiments, max_iter)

    def random_init(self, docs, doc_sentiments):
        for di in xrange(self.n_doc):
            self.sentiment_assigned.append(list())
            self.topic_assigned.append(list())
            doc = docs[di]
            sentiments = doc_sentiments[di]
            for w in doc:
                # random sampling topic
                z = np.random.choice(self.n_topic, 1)[0]
                # random sampling sentiment
                a = np.random.choice(len(sentiments), 1)[0]

                # assigning sampled value (sufficient statistics)
                self.TW[z, w] += 1
                self.ST[sentiments[a], z] += 1
                self.sum_T[z] += 1
                self.sum_S[sentiments[a]] += 1

                # keep sampled value for future sampling
                self.topic_assigned[di].append(z)
                self.sentiment_assigned[di].append(sentiments[a])

    def gibbs_sampling(self, docs, doc_sentiments, max_iter):
        for iter in xrange(max_iter):
            tic = time.time()
            for di in xrange(len(docs)):
                doc = docs[di]
                sentiments = doc_sentiments[di]

                for wi in xrange(len(doc)):
                    w = doc[wi]
                    old_z = self.topic_assigned[di][wi]
                    old_a = self.sentiment_assigned[di][wi]

                    self.TW[old_z, w] -= 1
                    self.ST[old_a, old_z] -= 1
                    self.sum_T[old_z] -= 1
                    self.sum_S[old_a] -= 1

                    wt = (self.TW[:, w] + self.beta) / (self.sum_T + self.n_voca * self.beta)
                    st = (self.ST[sentiments, :] + self.alpha) / (
                        self.sum_S[sentiments].repeat(self.n_topic).reshape(len(sentiments),
                                                                         self.n_topic) + self.n_topic * self.alpha)

                    pdf = st * wt
                    pdf = pdf.reshape(len(sentiments) * self.n_topic)
                    pdf = pdf / pdf.sum()

                    # sampling sentiment and topic
                    idx = np.random.multinomial(1, pdf).argmax()

                    new_ai = int(idx / self.n_topic)
                    new_topic = idx % self.n_topic

                    new_sentiment = sentiments[new_ai]
                    self.TW[new_topic, w] += 1
                    self.ST[new_sentiment, new_topic] += 1
                    self.sum_T[new_topic] += 1
                    self.sum_S[new_sentiment] += 1
                    self.topic_assigned[di][wi] = new_topic
                    self.sentiment_assigned[di][wi] = new_sentiment

            ll = self.log_likelihood()
            logger.info('[INIT] %d\telapsed_time:%.2f\tlog_likelihood:%.2f', iter, time.time() - tic, ll)

    def log_likelihood(self):
        ll = self.n_sentiments * gammaln(self.alpha * self.n_topic)
        ll -= self.n_sentiments * self.n_topic * gammaln(self.alpha)
        ll += self.n_topic * gammaln(self.beta * self.n_voca)
        ll -= self.n_topic * self.n_voca * gammaln(self.beta)

        for ai in xrange(self.n_sentiments):
            ll += gammaln(self.ST[ai, :]).sum() - gammaln(self.ST[ai, :].sum())
        for ti in xrange(self.n_topic):
            ll += gammaln(self.TW[ti, :]).sum() - gammaln(self.TW[ti, :].sum())

        return ll