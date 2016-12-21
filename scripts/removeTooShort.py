file = open("tokens.txt",'r')
lines = [line.rstrip('\n') for line in file]
ultimate = open("ultimate.txt",'w')
ultimate_sentiment = open('ultimate_sentiment.txt','w')

with open('sentimentlabel.txt') as f:
    sentiment = f.read().splitlines()
print(len(lines))
print (len(sentiment))
for i in range(len(lines)):
    if len(lines[i].strip()) < 10:
        continue
    else:
        ultimate.write(lines[i] + '\n')
        ultimate_sentiment.write(sentiment[i] + '\n')

ultimate.close()