import random
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from pycipher import SimpleSubstitution as SimpleSub
except ImportError:
    logger.error('pycipher is not installed. Install it with: pip install pycipher')
    exit(1)

try:
    from cryptoClasses.ngram_score import ngram_score
    import cryptoClasses.detectEnglish
except ImportError as e:
    logger.error('Failed to import cryptoClasses: %s', e)
    exit(1)

ngram = input('Please enter the name of the ngram file to try: ')

try:
    fitness = ngram_score(ngram)
except (FileNotFoundError, ValueError) as e:
    logger.error('Failed to load ngram file "%s": %s', ngram, e)
    exit(1)

file = input('Please enter the name of the encrypted text file to crack: ')
ctext = ''

try:
    with open(file, 'r') as f:
        ctext = f.read()
except FileNotFoundError:
    logger.error('Cipher text file not found: %s', file)
    exit(1)
except IOError as e:
    logger.error('Error reading cipher text file %s: %s', file, e)
    exit(1)

ctext = re.sub('[^A-Z]', '', ctext.upper())

if not ctext:
    logger.error('Cipher text file contains no alphabetic characters.')
    exit(1)

logger.debug('Loaded ciphertext of length %d from %s', len(ctext), file)

maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore, parentkey = maxscore, maxkey[:]
print("Substitution Cipher solver, you may have to wait several iterations")
print("for the correct result. Press ctrl+c to exit program.")

i = 0
while True:
    i = i + 1
    random.shuffle(parentkey)
    deciphered = SimpleSub(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        child = parentkey[:]
        child[a], child[b] = child[b], child[a]
        deciphered = SimpleSub(child).decipher(ctext)
        score = fitness.score(deciphered)
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count + 1
    if parentscore > maxscore:
        maxscore, maxkey = parentscore, parentkey[:]
        logger.info('New best score: %.2f on iteration %d', maxscore, i)
        print('\nbest score so far:', maxscore, 'on iteration', i)
        ss = SimpleSub(maxkey)
        print('    best key: ' + ''.join(maxkey))
        print('    plaintext: ' + ss.decipher(ctext))
