import re
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

message = 'prob2.5.9.txt'
pre = 'preamble.txt'
getty = 'getty.txt'

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error('File not found: %s', filename)
        exit(1)
    except IOError as e:
        logger.error('Error reading file %s: %s', filename, e)
        exit(1)

logger.debug('Reading input files: %s, %s, %s', message, pre, getty)

m = re.sub('[^A-Z]', '', read_file(message).upper())
p = re.sub('[^A-Z]', '', read_file(pre).upper())
g = re.sub('[^A-Z]', '', read_file(getty).upper())

if not m:
    logger.error('Message file "%s" contains no alphabetic characters.', message)
    exit(1)

if len(p) < len(m) or len(g) < len(m):
    logger.error('Key files are shorter than the message (msg=%d, preamble=%d, getty=%d). Cannot decrypt.',
                 len(m), len(p), len(g))
    exit(1)

logger.debug('Message length: %d, preamble length: %d, getty length: %d', len(m), len(p), len(g))

pos = 0
text = ''

for ch in m:
    decoded = ((ord(ch) - 65) - (ord(p[pos]) - 65) - (ord(g[pos]) - 65)) % 26
    decoded = chr(decoded + 65)
    text = text + decoded
    pos += 1

print(text)

try:
    with open('prob2.5.9.Out.txt', 'w') as out:
        out.write(text)
    logger.info('Output written to prob2.5.9.Out.txt')
except IOError as e:
    logger.error('Error writing output file: %s', e)
