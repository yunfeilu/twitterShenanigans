file = open('ultimate.txt','r')

voc = []
tot_num = 0
for line in file:
    temp = line.split()
    for word in temp:
        tot_num += 1
        if word not in voc:
            voc.append(word)

print(len(voc))
print (tot_num)

