#include<stdio.h>
#include<stdlib.h>

cypherText = input('Please enter the string to encode/decode: ')

l = len(cypherText)
i = 0
cypherList = list(cypherText)

#print(cypherText)
#print(cypherList[0])
out = list('')

while i < l:
        c = cypherText[i]

        if (ord(c) >= ord('a') and ord(c) <= ord('z')):
            out.append('%c'% (chr(ord('z') - (ord(c) - ord('a')))))
            #print('if')
        elif (ord(c) >= ord('A') and ord(c) <= ord('Z')):
            out.append('%c'% (chr(ord('Z') - (ord(c) - ord('A')))))
            #print('elif')
        else:
            out.append(c)
            #print(c)

        i += 1

print(''.join(out))


