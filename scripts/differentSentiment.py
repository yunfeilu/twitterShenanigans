file = open("ultimate.txt",'r')
lines = [line.rstrip('\n') for line in file]
with open('ultimate_sentiment.txt') as f:
    ultimate_sentiment = f.read().splitlines()


ultimate_pos = open('ultimate_pos.txt','w')
ultimate_neg = open('ultimate_neg.txt','w')
ultimate_neu = open('ultimate_neu.txt','w')

for i in range(len(ultimate_sentiment)):
    if ultimate_sentiment[i] is '2':
        ultimate_pos.write(lines[i] + '\n')
    elif ultimate_sentiment[i] is '1':
        ultimate_neu.write(lines[i] + '\n')
    else:
        ultimate_neg.write(lines[i] + '\n')