import sys, re, math
import logging
from cryptoClasses.gcdEuclid import gcdEuclid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

""" m = pq p and q are two prime integers
    n = (p -1)(q - 1)
    d = e^-1 mod n
    e = public key which must be relatively prime to pq"""

class RSA:

    def isPrime(self, num):
        if num < 2:
            return False
        for i in range(2, math.ceil(math.sqrt(num)) + 1):
            if (num % i) == 0:
                return False
        return True

    def encrypt(self, message, e, m):
        num = message
        for i in range(0, e - 1):
            num = num * message
        return num % m

    def decrypt(self, message, d, m):
        num = message
        for i in range(0, d - 1):
            num = num * message
        return num % m

    def detD(self, e, n):
        gE = gcdEuclid()
        out = gE.ext_euclid(e, n)
        if out is None:
            logger.error('detD: ext_euclid returned None for e=%d, n=%d.', e, n)
            return 0
        inverseE = out['t']
        return inverseE % n

    def detM(self, p, q):
        return p * q

    def detN(self, p, q):
        return (p - 1) * (q - 1)

    def charToInt(self, message):
        out = []
        for ch in message:
            out.append(ord(ch) - 65)
        return out

    def covertToBase(self, n, b):
        out = []
        if n == 0:
            return [0]
        while n:
            out.append(n % b)
            n //= b
        return out[::-1]

    def run(self):
        rsa = RSA()

        while True:
            try:
                p = int(input('Please enter the first prime: '))
            except ValueError:
                logger.error('p must be an integer.')
                continue
            if not rsa.isPrime(p):
                logger.warning('First number %d is not prime.', p)
                print('First number is not prime.')
                continue

            try:
                q = int(input('Please enter the second prime: '))
            except ValueError:
                logger.error('q must be an integer.')
                continue
            if not rsa.isPrime(q):
                logger.warning('Second number %d is not prime.', q)
                print('Second number is not prime.')
                continue

            try:
                e = int(input('Please input the public key: '))
            except ValueError:
                logger.error('Public key must be an integer.')
                continue

            break

        m_val = rsa.detM(p, q)
        n_val = rsa.detN(p, q)
        d_val = rsa.detD(e, n_val)
        logger.debug('RSA parameters: p=%d, q=%d, m=%d, n=%d, d=%d', p, q, m_val, n_val, d_val)
        print('p = %d q = %d m = %d n = %d d = %d' % (p, q, m_val, n_val, d_val))

        try:
            blockSize = int(input('Please enter the block size: '))
            decision = int(input("Enter 1 for encode or 2 for decode: "))
        except ValueError:
            logger.error('Block size and decision must be integers.')
            return

        if decision not in (1, 2):
            logger.error('Decision must be 1 (encode) or 2 (decode), got %d.', decision)
            return

        if blockSize <= 0:
            logger.error('Block size must be a positive integer, got %d.', blockSize)
            return

        message = input('Please enter the message: ')

        if not message.strip():
            logger.error('Message cannot be empty.')
            return

        if decision == 1:
            message = re.sub('[^A-Z]', '', message.upper())
            if not message:
                logger.error('Message contains no alphabetic characters.')
                return

            logger.debug('Encoding message of length %d with block size %d', len(message), blockSize)
            out = []
            text = rsa.charToInt(message)
            total = 0
            power = blockSize - 1

            for i in range(1, len(text) + 1):
                if i % blockSize == 0:
                    total += text[i - 1] * int(math.pow(26, power))
                    out.append(int(total))
                    total = 0
                    power = blockSize - 1
                else:
                    total += text[i - 1] * int(math.pow(26, power))
                    power -= 1

            for i in range(0, len(out)):
                out[i] = rsa.encrypt(out[i], e, m_val)

            print('Output: ', end='')
            for i in range(0, len(out)):
                print(out[i], end=' ')
            print('')
            logger.info('Encoding complete. %d blocks output.', len(out))

        else:
            logger.debug('Decoding message with block size %d', blockSize)
            text = []
            temp = ''

            for ch in message:
                if ch != ' ':
                    temp = temp + ch
                else:
                    if temp:
                        try:
                            text.append(int(temp))
                        except ValueError:
                            logger.error('Invalid numeric value in message: "%s"', temp)
                            return
                    temp = ''

            if temp:
                try:
                    text.append(int(temp))
                except ValueError:
                    logger.error('Invalid numeric value in message: "%s"', temp)
                    return

            for i in range(0, len(text)):
                text[i] = rsa.decrypt(text[i], d_val, m_val)

            out = []
            for i in range(0, len(text)):
                temp = rsa.covertToBase(text[i], 26)
                while len(temp) != blockSize:
                    temp = [0] + temp
                for x in range(0, len(temp)):
                    out.append(temp[x])

            for i in range(0, len(out)):
                print(chr(out[i] + 65), end='')
            print('')
            logger.info('Decoding complete.')

if __name__ == '__main__':
    RSA().run()
