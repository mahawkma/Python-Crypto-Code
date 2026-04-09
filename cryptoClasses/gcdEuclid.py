import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class gcdEuclid:
    #Iterative Euclidean Algorithm
    def gcdIter(self, a, b):
        if b == 0:
            return a
        else:
            gE = gcdEuclid()
            return gE.gcdIter(b, a % b)

    #Extended Euclidean Algorithm
    def ext_euclid(self, a, b):
        """Extended Euclid's algorithm for GCD.
        Given input a, b the function returns d such that gcd(a,b) = d
        and s, t such that as + bt = d, as well as u, v such that au = bv."""
        gE = gcdEuclid()

        if a == 0 and b == 0:
            logger.error('ext_euclid called with both a and b equal to 0.')
            return None

        if a < b:
            a, b = b, a

        A = a
        B = b
        u, v, s, t = 0, 1, 1, 0

        while b != 0:
            a, b, s, t, u, v = b, a % b, u, v, s - (a // b) * u, t - (a // b) * v

        out = {'a': a, 'b': b, 's': s, 't': t, 'u': u, 'v': v}

        logger.debug('ext_euclid: %d*%d + %d*%d = %d', A, s, B, t, gE.gcdIter(A, B))
        print('%d*%d + %d*%d = %d' % (A, s, B, t, gE.gcdIter(A, B)))

        return out

    def run(self):
        gE = gcdEuclid()

        try:
            a = int(input('Please enter first integer: '))
            b = int(input('Please enter second integer: '))
        except ValueError:
            logger.error('Both inputs must be integers.')
            return

        if a == 0 and b == 0:
            logger.error('Both inputs cannot be zero.')
            return

        logger.debug('Computing GCD of %d and %d', a, b)
        gcd = gE.gcdIter(a, b)
        print('gcd of %d and %d is %d.' % (a, b, gcd))
        logger.info('GCD(%d, %d) = %d', a, b, gcd)

        gE.ext_euclid(a, b)

if __name__ == "__main__":
    gcdEuclid().run()
