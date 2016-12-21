from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
line_number = 1
file = open('doc.txt','r')



with open('doc.txt','r') as f:
    documents = f.read().splitlines()

# sentences = ["VADER is smart, handsome, and funny.",
#              "VADER is not smart, handsome, nor funny.",
#              "VADER is smart, handsome, and funny!",
#              "VADER is very smart, handsome, and funny.",
#              "VADER is VERY SMART, handsome, and FUNNY."]
analyzer = SentimentIntensityAnalyzer()
sentiment_label = open('sentimentlabel.txt','w')
for sentence in documents:
    vs = analyzer.polarity_scores(sentence)
    if vs['pos'] >= vs['neg'] and vs['pos'] >= vs['neu']:
        sentiment_label.write(str(2) + '\n')
    elif vs['neg'] >=  vs['pos'] and vs ['neg'] >= vs['neu']:
        sentiment_label.write(str(0) + '\n')
    elif vs['neu'] >= vs['pos'] and vs['neu'] >= vs['neg']:
        sentiment_label.write(str(1) + '\n')
