import re
import sys

message = 'prob2.5.9.txt'
pre = 'preamble.txt'
getty = 'getty.txt'

text = ''
ctext = ''

with open(message, 'r') as f:
            text = f.read()
            ctext = ctext + text

m = ctext
ctext = ''
text = ''

with open(pre, 'r') as f:
            text = f.read()
            ctext = ctext + text

p = ctext
ctext = ''
text = ''

with open(getty, 'r') as f:
            text = f.read()
            ctext = ctext + text

g = ctext

out = open('prob2.5.9.Out.txt', 'w')

m = re.sub('[^A-Z]','', m.upper())
p = re.sub('[^A-Z]','', p.upper())
g =re.sub('[^A-Z]','', g.upper())

pos = 0
text = ''


for ch in m:
    #print(ch)
    decoded = ( (ord(ch) - 65) - (ord(p[pos]) - 65) - (ord(g[pos]) - 65) )%26
    decoded = chr(decoded + 65)
    #print(decoded)
    text = text + decoded
    pos += 1

print(text)
out.write(text)

out.close()