
#!/usr/bin/env python3

from string import ascii_lowercase
import sys
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


###### HELPER FUNCTIONS ######

def scrubstring(s):
    """Takes a string, s, and returns that string after conversion to lowercase
    and with all characters not present in ascii_lowercase removed. Examples:

    'Test!!' -> 'test'
    'I'm' -> 'im'
    'Don't use multiple words...' -> 'dontusemultiplewords'"""

    return ''.join(ch for ch in s.lower() if ch in ascii_lowercase)

def getpatterntuple(word):
    """Takes a string and returns a tuple which retains only character
    repetition info. Examples:
    'word'  -> (1, 2, 3, 4)
    'all'   -> (1, 2, 2)
    'llama' -> (1, 1, 2, 3, 2)"""

    word = word.lower()
    letters = {}
    tup = ()

    for letter in word:
        if letter in letters:
            tup += (letters[letter],)
        else:
            letternum = len(letters) + 1
            tup += (letternum,)
            letters[letter] = letternum

    return tup

def getregex(cipherword, subs):
    """Given a ciphertext word and a dictionary of ciphertext-to-plaintext
    substitutions, returns a regex that matches all and only those words which,
    given additionally that their letter repetition patterns are correct, could
    be the plaintext."""

    if len(subs) > 0:
        wildcard = "[^"+"".join(str(n) for n in subs.values())+"]"
    else:
        wildcard = "."

    regex = "".join(wildcard if ch not in subs else subs[ch] for ch in cipherword)
    return re.compile("^%s$"%(regex,))

def getsubs(cipherwords, guess):
    """Takes a list or tuple of ciphertext words and a list or tuple which is
    the current guess, and returns a dictionary describing every substitution
    assumed by this guess."""
    subs = {}

    for wordind in range(len(guess)):
        for letterind in range(len(guess[wordind])):
            subs[cipherwords[wordind][letterind]] = guess[wordind][letterind]

    return subs

def prettyprint(ciphertext, substitutions):
    """Takes a dictionary of substitutions and performs them to the original
    ciphertext for a readable result."""

    ans = ""
    for ch in ciphertext:
        if ch.lower() in substitutions:
            if ch in ascii_lowercase:
                ans += substitutions[ch]
            else:
                ans += substitutions[ch.lower()].upper()
        else:
            ans += ch

    return ans


###### BODY -- LOADING DICTIONARY FILE ######

dictfile = '/usr/share/dict/words'
patterns = {}

try:
    with open(dictfile, 'r') as f:
        for line in f:
            line = scrubstring(line)
            tup = getpatterntuple(line)
            if tup in patterns:
                if line not in patterns[tup]:
                    patterns[tup].append(line)
            else:
                patterns[tup] = [line]
    logger.info('Dictionary loaded from %s (%d patterns)', dictfile, len(patterns))
except FileNotFoundError:
    logger.error('Dictionary file not found: %s', dictfile)
    sys.exit(1)
except IOError as e:
    logger.error('Error reading dictionary file %s: %s', dictfile, e)
    sys.exit(1)

print("Dictionary file loaded.")


###### BODY -- CRACKING THE CODE ######

if len(sys.argv) < 2:
    ciphertext = "pf mmwpw skmms fjppf kkms" # same as in the blog's example
else:
    ciphertext = ' '.join(sys.argv[1:])

print("Ciphertext: " + ciphertext)
print("Cracking...")

cipherlist = [scrubstring(word) for word in ciphertext.split(' ')
              if scrubstring(word) != '']

if not cipherlist:
    logger.error('Ciphertext contains no valid words after scrubbing.')
    sys.exit(1)

logger.debug('Cracking %d words: %s', len(cipherlist), cipherlist)

# each entry on the stack is a tuple of guessed plaintext words
stack = [()]
possibilities = []

while stack:
    currguess = stack.pop()
    ind = len(currguess)

    if ind == len(cipherlist):
        possibilities.append(currguess)

        if len(possibilities) >= 15:
            print("Possibilities abound! We're calling the search off early.")
            break

        continue

    subs = getsubs(cipherlist, currguess)
    wordtuple = getpatterntuple(cipherlist[ind])

    if wordtuple not in patterns:
        logger.debug('No dictionary matches for word "%s".', cipherlist[ind])
        continue

    regex = getregex(cipherlist[ind], subs)

    for guess in patterns[wordtuple]:
        if regex.match(guess):
            stack.append(currguess + (guess,))


###### BODY -- BOASTING OF OUR GLORIOUS SUCCESS ######

if len(possibilities) == 0:
    logger.warning('No answers found.')
    print("No answers found... Perhaps one of the plaintext words isn't in our dictionary?")
elif len(possibilities) == 1:
    solution = prettyprint(ciphertext, getsubs(cipherlist, possibilities[0]))
    logger.info('Unique solution found: %s', solution)
    print("We've got it!\n")
    print(solution)
else:
    logger.info('%d possible solutions found.', len(possibilities))
    print("Yee dawgies!")
    print("We've got more possible solutions than we know what to do with.")
    print("Here's %s of them:\n"%(len(possibilities),))

    for possibility in possibilities:
        print(ciphertext, getsubs(cipherlist, possibility))
