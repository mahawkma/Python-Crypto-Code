import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cypherText = input('Please enter the string to encode/decode: ')

if not cypherText:
    logger.error('Input string is empty.')
    exit(1)

logger.debug('Applying Atbash cipher to text of length %d', len(cypherText))

l = len(cypherText)
i = 0
out = list('')

while i < l:
    c = cypherText[i]

    if ord('a') <= ord(c) <= ord('z'):
        out.append('%c' % (chr(ord('z') - (ord(c) - ord('a')))))
    elif ord('A') <= ord(c) <= ord('Z'):
        out.append('%c' % (chr(ord('Z') - (ord(c) - ord('A')))))
    else:
        out.append(c)

    i += 1

result = ''.join(out)
logger.info('Atbash cipher applied successfully.')
print(result)
