#include<stdio.h>
#include<stdlib.h>

cypherText = input('Please enter string to decode: ')
lines = int(input('Please enter the number of lines: '))
l = list(cypherText)
out = list('')
place = 0

while place < lines:
    j = place
    while j < len(cypherText):
        out.append(l[j])
        j += lines
    place += 1

print (''.join(out))
        
