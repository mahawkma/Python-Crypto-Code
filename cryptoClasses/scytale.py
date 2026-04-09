import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    cypherText = input('Please enter string to decode: ')
    lines = int(input('Please enter the number of lines: '))
except ValueError:
    logger.error('Number of lines must be an integer.')
    exit(1)

if not cypherText:
    logger.error('Input string is empty.')
    exit(1)

if lines <= 0:
    logger.error('Number of lines must be a positive integer.')
    exit(1)

logger.debug('Decoding scytale cipher: text length=%d, lines=%d', len(cypherText), lines)

l = list(cypherText)
out = list('')
place = 0

while place < lines:
    j = place
    while j < len(cypherText):
        out.append(l[j])
        j += lines
    place += 1

result = ''.join(out)
logger.info('Decoding complete.')
print(result)
