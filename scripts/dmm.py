from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import utility
import string
import operator

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    # doc = " ".join(doc)
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
	# singles = " ".join(stemmer.stem(plural) for plural in punc_free.split())
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


class GibbsSamplingDMM:
    def __init__(self, pathToCorpus, inNumTopics, inAlpha, inBeta, inNumIterations, inTopWords, inExpName, inSaveStep):
        self.alpha = inAlpha
        self.beta = inBeta
        self.numTopics = inNumTopics
        self.numIterations = inNumIterations
        self.topWords = inTopWords
        self.savestep = inSaveStep
        self.expName = inExpName
        self.orgExpName = expName
        self.corpusPath = pathToCorpus
        self.folderPath = pathToCorpus  #############################
        print ("Reading topic modeling corpus: " + pathToCorpus)
        self.word2IdVocabulary = {}
        self.id2WordVocabulary = {}
        self.corpus = []
        self.occurenceToIndexCount = []
        self.numDocuments = 0
        self.numWordsInCorpus = 0
        index_word = -1
        with open(pathToCorpus) as f:
            for line in f:
                line = clean(line)
                if len(line.split()) == 0:
                    continue
                words = line.split()
                documents = []
                wordOccurenceToIndexInDoc = []
                wordOccurenceToIndexInDocCount = {}
                for word in words:
                    if word in self.word2IdVocabulary:
                        documents.append(self.word2IdVocabulary[word])
                    else:
                        index_word += 1
                        self.word2IdVocabulary[word] = index_word
                        self.id2WordVocabulary[index_word] = word
                        documents.append(index_word)
                    times = 0
                    if word in wordOccurenceToIndexInDocCount:
                        times = wordOccurenceToIndexInDoc[word]
                    times += 1
                    wordOccurenceToIndexInDocCount[word] = times
                    wordOccurenceToIndexInDoc.append(times)
                self.numDocuments += 1
                self.numWordsInCorpus += len(documents)
                self.corpus.append(documents)
                self.occurenceToIndexCount.append(wordOccurenceToIndexInDoc)
        self.vocabularySize = len(self.word2IdVocabulary)
        self.docTopicCount = []
        self.topicWordCount = []
        self.sumTopicWordCount = []
        self.multiPros = []
        for i in range(0, self.numTopics):
            self.multiPros[i] = 1.0 / self.numTopics
        self.alphaSum = self.numTopics * self.alpha
        self.betaSum = self.vocabularySize * self.beta
        print("Corpus size: " + self.numDocuments + " docs, "
              + self.numWordsInCorpus + " words")
        print ("Vocabuary size: " + self.vocabularySize)
        print("Number of topics: " + self.numTopics)
        print("alpha: " + self.alpha)
        print("beta: " + self.beta)
        print("Number of sampling iterations: " + self.numIterations)
        print("Number of top topical words: " + self.topWords)
        print("Randomly initialzing topic assignments ...")
        self.topicAssignments = []
        for i in range(0, self.numDocuments):
            topic = utility.nextDiscrete(self.multiPros)
            self.docTopicCount[topic] += 1
            docSize = len(self.corpus[i])
            for j in range(0, docSize):
                self.topicWordCount[topic][self.corpus[i][j]] += 1
                self.sumTopicWordCount[topic] += 1
                self.topicAssignments.append(topic)

    def inference(self):
        writeParameters()
        writeDictionary()
        print ("Running Gibbs sampling inference: ")
        for i in range(1, self.numIterations + 1):
            print("\tSampling iteration: " + iter)
            sampleInSingleIteration()
            if self.savestep > 0 and iter % self.savestep == 0 and iter < self.numIterations:
                print("\t\tSaving the output from the " + iter + "^{th} sample")
                self.expName = self.orgExpName + "-" + iter
                write()
        self.expName = self.orgExpName
        print("Writing output from the last sample ...")
        write()
        print("Sampling completed!")

    def sampleInSingleIteration(self):
        for dIndex in range(0, self.numDocuments):
            topic = self.topicAssignments[dIndex]
            document = self.corpus[dIndex]
            docSize = len(document)

            self.docTopicCount[topic] -= 1
            for wIndex in range(0, docSize):
                word = document[wIndex]
                self.topicWordCount[topic][word] -= 1
                self.sumTopicWordCount[topic] -= 1
                ## sample a topic
            for tIndex in range(0, self.numTopics):
                self.multiPros[tIndex] = self.docTopicCount[tIndex] + self.alpha
                for wIndex in range(0, docSize):
                    word = document[wIndex]
                    self.multiPros[tIndex] *= (self.topicWordCount[tIndex][word] + self.beta +
                                               self.occurenceToIndexCount[dIndex][wIndex] - 1) / (
                                              self.sumTopicWordCount[tIndex] + self.betaSum + wIndex)
            topic = utility.nextDiscrete(self.multiPros)
            self.docTopicCount[topic] += 1
            for wIndex in range(0, docSize):
                word = document[wIndex]
                self.topicWordCount[topic][word] += 1
                self.sumTopicWordCount[topic] += 1
            self.topicAssignments[dIndex] = topic

    def writeParameters(self):
		writer = open(self.folderPath + self.expName + ".paras", 'w')
		writer.write("-model" + "\t" + "DMM")
		writer.write("\n-corpus" + "\t" + self.corpusPath)
		writer.write("\n-ntopics" + "\t" + self.numTopics)
		writer.write("\n-alpha" + "\t" + self.alpha)
		writer.write("\n-beta" + "\t" + self.beta)
		writer.write("\n-niters" + "\t" + self.numIterations)
		writer.write("\n-twords" + "\t" + self.topWords)
		writer.write("\n-name" + "\t" + self.expName)
		writer.write("\n-sstep" + "\t" + self.savestep)
		writer.close()

	def writeDictionary(self):
		writer = open(self.folderPath + self.expName + ".vocabulary", 'w')
		for id in range(0,self.vocabularySize):
			writer.write(self.id2WordVocabulary[id] + " " + id + "\n")
		writer.close()

	def writeIDbasedCorpus(self):
		writer = open(self.folderPath + self.expName + ".IDcorpus")
		for dIndex in range(0,self.numDocuments):
			docSize = len(self.corpus[dIndex])
			for wIndex in range(0, docSize):
				writer.write(self.corpus[dIndex][wIndex] + " ")
			writer.write("\n")
		writer.close()

	def writeTopicAssignments(self):
		writer = open(self.folderPath + self.expName + ".topicAssignments")
		for dIndex in range(0, self.numDocuments):
			docSize = len(self.corpus[dIndex])
			topic = self.topicAssignments[dIndex]
			for wIndex in range(0,docSize):
				writer.write(topic + " ")
			writer.write("\n")
		writer.close()

	def writeTopTopicalWords(self):
		writer = open(self.folderPath + self.expName + ".topWords")
		for tIndex in range(0,self.numTopics):
			writer.write("Topic" + tIndex + ":")
			wordCount = {}
			for wIndex in range(0,self.vocabularySize):
				wordCount[wIndex] = self.topicWordCount[tIndex][wIndex]
			sorted_wordCount = sorted(wordCount.items(), key=operator.itemgetter(1),reverse=True)
			mostLikelyWords = [item[0] for item in sorted_wordCount]
			count = 0
			for index in mostLikelyWords:
				if count < self.topWords:
					pro = (self.topicWordCount[tIndex][index] + self.beta) / (self.sumTopicWordCount[tIndex] + self.betaSum)
					pro = round(pro * 1000000.0) / 1000000.0
					writer.write(" " + self.id2WordVocabulary[index] + "(" + pro + ")")
					count += 1
				else:
					writer.write("\n")
					break
		writer.close()

	def writeTopicWordPros(self):
		writer = open(self.folderPath + self.expName + ".phi")
		for i in range(0,self.numTopics):
			for j in range(0,self.vocabularySize):
				pro = (self.topicWordCount[i][j] + self.beta) / (self.sumTopicWordCount[i] + self.betaSum)
				writer.write(pro + " ")
			writer.write("\n")
		writer.close()

	def writeTopicWordCount(self):
		writer = open(self.folderPath + self.expName + ".WTcount")
		for i in range(0,self.numTopics):
			for j in range(0,self.vocabularySize):
				writer.write(self.topicWordCount[i][j] + " ")
			writer.write("\n")
		writer.close()

	def writeDocTopicPros(self):
		writer = open(self.folderPath + self.expName + ".theta")
		for i in range(0,self.numDocuments):
			docSize = len(self.corpus[i])
			sum_val = 0.0
			for tIndex in range(0, self.numTopics):
				self.multiPros[tIndex] = self.docTopicCount[tIndex] + self.alpha
				for wIndex in range(0,docSize):
					word = self.corpus[i][wIndex]
					self.multiPros[tIndex] *= (self.topicWordCount[tIndex][word] + self.beta) / (self.sumTopicWordCount[tIndex] + self.betaSum)
				sum_val += self.multiPros[tIndex]
			for tIndex in range(0, self.numTopics):
				writer.write(self.multiPros[tIndex] / sum_val + " ")
			writer.write("\n")
		writer.close()
	def write_result(self):
		self.writeTopTopicalWords()
		self.writeDocTopicPros()
		self.writeTopicAssignments()
		self.writeTopicWordPros()


model = GibbsSamplingDMM("test/corpus.txt",7, 0.1, 0.1, 2000, 20, "testDMM")
model.inference()





