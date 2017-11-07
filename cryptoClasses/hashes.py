import sys, re

inPut = []
output = ''
temp = 0
count = 0
text = input('Please enter the damn string to hash: ')

text = re.sub('[^A-Z]','',text.upper()) #Make sure there are no spaces and that all chars are upper case

while len(text)%5 != 0: #Pad the string if needed
    text = text + 'X'

for ch in text: #append the chars with A = 0 to the list
    inPut.append(ord(ch) - 65)

while count < 5: #for every 5 chars
    for i in range(len(inPut)):
        if i%5 == count:
            temp = temp + inPut[i]
            #print('input = %d temp = %d'%(inPut[i],temp))

    output = output + chr(temp%26 + 65)
    #print('output = %s'%output)

    temp = 0
    count += 1
    

print('Hash = %s'%output)