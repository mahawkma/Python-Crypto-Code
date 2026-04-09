import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    sharedPrime = int(input("Please enter the shared prime: "))
    sharedBase = int(input("Please enter shared base: "))
    firstSecret = int(input("Please enter the first secret: "))
    secondSecret = int(input("Please enter the second secret: "))
except ValueError:
    logger.error('All inputs must be integers.')
    exit(1)

if sharedPrime < 2:
    logger.error('Shared prime must be greater than 1, got %d.', sharedPrime)
    exit(1)

logger.debug('Diffie-Hellman: prime=%d, base=%d, s1=%d, s2=%d',
             sharedPrime, sharedBase, firstSecret, secondSecret)

alpha = (sharedBase ** firstSecret) % sharedPrime
beta = (sharedBase ** secondSecret) % sharedPrime

kBeta = (beta ** firstSecret) % sharedPrime
kAlpha = (alpha ** secondSecret) % sharedPrime

if kBeta != kAlpha:
    logger.warning('Shared secrets do not match: kBeta=%d, kAlpha=%d', kBeta, kAlpha)
else:
    logger.info('Shared secret successfully established: %d', kBeta)

print("alpha = %d beta = %d kBeta = %d kAlpha = %d" % (alpha, beta, kBeta, kAlpha))
