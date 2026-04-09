'''
Allows scoring of text using n-gram probabilities
17/07/12
'''
from math import log10
import logging

logger = logging.getLogger(__name__)

class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        key = None
        try:
            with open(ngramfile, 'r') as file:
                for line in file:
                    key, count = line.split(sep)
                    self.ngrams[key] = int(count)
        except FileNotFoundError:
            logger.error('Ngram file not found: %s', ngramfile)
            raise
        except IOError as e:
            logger.error('Error reading ngram file %s: %s', ngramfile, e)
            raise
        except ValueError as e:
            logger.error('Malformed line in ngram file %s: %s', ngramfile, e)
            raise

        if not self.ngrams:
            logger.error('Ngram file %s is empty or contains no valid entries.', ngramfile)
            raise ValueError('Ngram file is empty')

        self.L = len(key)
        self.N = sum(self.ngrams.values())
        for key in self.ngrams:
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)
        logger.debug('Loaded %d ngrams of length %d from %s', len(self.ngrams), self.L, ngramfile)

    def score(self, text):
        ''' compute the score of text '''
        if not text:
            logger.warning('score() called with empty text.')
            return self.floor
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i+self.L] in self.ngrams:
                score += ngrams(text[i:i+self.L])
            else:
                score += self.floor
        return score
