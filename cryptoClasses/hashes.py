import sys, re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

inPut = []
output = ''
temp = 0
count = 0

text = input('Please enter the string to hash: ')

if not text.strip():
    logger.error('Input string is empty.')
    exit(1)

text = re.sub('[^A-Z]', '', text.upper())

if not text:
    logger.error('Input contains no alphabetic characters.')
    exit(1)

logger.debug('Hashing text of length %d (after stripping non-alpha)', len(text))

while len(text) % 5 != 0:
    text = text + 'X'

for ch in text:
    inPut.append(ord(ch) - 65)

while count < 5:
    for i in range(len(inPut)):
        if i % 5 == count:
            temp = temp + inPut[i]

    output = output + chr(temp % 26 + 65)
    temp = 0
    count += 1

logger.info('Hash computed: %s', output)
print('Hash = %s' % output)
