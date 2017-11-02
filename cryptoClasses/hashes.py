import sys, re

inPut = []
output = ''
temp = 0
count = 0
text = input('Please enter the damn string to hash: ')

text = re.sub('[^A-Z]','',text.upper())

while len(text)%5 != 0:
    text = text + 'X'

for ch in text:
    inPut.append(ord(ch) - 65)

while count < 5:
    for i in range(len(inPut)):
        if i%5 == count:
            temp = temp + inPut[i]
            #print('input = %d temp = %d'%(inPut[i],temp))

    output = output + chr(temp%26 + 65)
    #print('output = %s'%output)

    temp = 0
    count += 1
    

print('Hash = %s'%output)