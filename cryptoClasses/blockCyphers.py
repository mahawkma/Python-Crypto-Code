import sys, re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class blockCyphers:

    dicS = {'000': '11', '001': '01', '010 ': '00', '011': '10', '100': '01', '101': '00', '110': '11', '111': '10'}

    #Convert binary text to a list of integers.
    def convertStringList(self, text):
        binaryList = []
        for ch in text:
            if ch not in ('0', '1'):
                logger.error('Non-binary character "%s" in input.', ch)
                return []
            binaryList.append(int(ch))
        return binaryList

    #Calculate the t values for the computation using the block, its key, and the inverse value.
    def tValues(self, block, key, inverse):
        bc = blockCyphers()
        dicS = {'000': '11', '001': '01', '010': '00', '011': '10', '100': '01', '101': '00', '110': '11', '111': '10'}
        S = []
        stringS = ''

        if inverse == 1:
            S.append(block[2] ^ key[0])
            S.append(block[3] ^ key[1])
            S.append(block[2] ^ key[2])
        else:
            S.append(block[0] ^ key[0])
            S.append(block[1] ^ key[1])
            S.append(block[0] ^ key[2])

        for i in range(len(S)):
            stringS = stringS + str(S[i])

        if stringS not in dicS:
            logger.error('S-box lookup failed for key "%s".', stringS)
            return []

        return bc.convertStringList(dicS[stringS])

    #Calculate the u values given the block, the t values, and the inverse value.
    def uValues(self, block, t, inverse):
        u = []
        if inverse == 1:
            u.append(block[0] ^ t[0])
            u.append(block[1] ^ t[1])
        else:
            u.append(block[2] ^ t[0])
            u.append(block[3] ^ t[1])
        return u

    #Compute the encrypted or decrypted message given the block, the key, and the inverse value.
    def compute(self, block, key, inverse):
        bc = blockCyphers()
        t = bc.tValues(block, key, inverse)
        if not t:
            logger.error('compute: tValues returned empty result.')
            return []
        u = bc.uValues(block, t, inverse)
        if inverse == 1:
            return [block[2], block[3], u[0], u[1]]
        else:
            return [u[0], u[1], block[0], block[1]]

    def run(self):
        try:
            mode = int(input('Please enter 1 for block mode, 2 for CBC mode, & 3 for CFB mode: '))
        except ValueError:
            logger.error('Mode must be an integer (1, 2, or 3).')
            return

        if mode not in (1, 2, 3):
            logger.error('Invalid mode %d. Must be 1, 2, or 3.', mode)
            return

        bc = blockCyphers()

        if mode == 1:  # Block Mode
            bString = re.sub('[^01]', '', input('Please enter 4 bit block: '))
            kString = re.sub('[^01]', '', input('Please enter the 3 bit key: '))
            try:
                Round = int(input('Please enter the number of rounds: '))
                inverse = int(input('Please enter 1 for non-inverse and 0 for inverse: '))
            except ValueError:
                logger.error('Rounds and inverse must be integers.')
                return

            if len(bString) != 4:
                logger.error('Block must be exactly 4 bits, got %d.', len(bString))
                return
            if len(kString) != 3:
                logger.error('Key must be exactly 3 bits, got %d.', len(kString))
                return
            if inverse not in (0, 1):
                logger.error('Inverse must be 0 or 1.')
                return

            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)
            logger.debug('Block mode: block=%s, key=%s, rounds=%d, inverse=%d', bString, kString, Round, inverse)

            for i in range(Round):
                block = bc.compute(block, key, inverse)
                if not block:
                    logger.error('Computation failed at round %d.', i + 1)
                    return

            print(block)

        elif mode == 2:  # CBC Mode
            bString = re.sub('[^01]', '', input('Please enter input binary string: '))
            kString = re.sub('[^01]', '', input('Please enter the 3 bit key: '))
            try:
                inverse = int(input('Please enter 1 for non-inverse and 0 for inverse: '))
                Round = int(input('Please enter the number of rounds: '))
            except ValueError:
                logger.error('Inverse and rounds must be integers.')
                return

            if len(kString) != 3:
                logger.error('Key must be exactly 3 bits, got %d.', len(kString))
                return
            if inverse not in (0, 1):
                logger.error('Inverse must be 0 or 1.')
                return
            if len(bString) == 0 or len(bString) % 4 != 0:
                logger.error('Input binary string length must be a non-zero multiple of 4, got %d.', len(bString))
                return

            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)
            logger.debug('CBC mode: key=%s, rounds=%d, inverse=%d, block_len=%d', kString, Round, inverse, len(block))

            temp = [0, 0, 0, 0]
            y = []
            inv = []
            pointer = 0
            out = ''

            while pointer < 4:
                y.append(block[pointer])
                pointer += 1

            if inverse == 1:
                for i in range(int(len(block) / 4)):
                    for i in range(Round):
                        y = bc.compute(y, key, inverse)
                        if not y:
                            logger.error('CBC computation failed.')
                            return

                    for i in range(4):
                        out = out + str(y[i])
                    out = out + ' '

                    if pointer >= len(block) - 1:
                        continue

                    for j in range(4):
                        temp[j] = block[pointer]
                        pointer += 1

                    for k in range(4):
                        y[k] = y[k] ^ temp[k]

                print(out)

            else:
                for i in range(Round):
                    inv = bc.compute(y, key, inverse)

                for i in range(4):
                    out = out + str(inv[i])
                out = out + ' '

                for i in range(1, int(len(block) / 4)):
                    for x in range(4):
                        temp[x] = y[x]

                    for j in range(4):
                        y[j] = block[pointer]
                        pointer += 1

                    print('y = ' + str(y))
                    inv = y

                    for i in range(Round):
                        inv = bc.compute(inv, key, inverse)

                    for k in range(4):
                        inv[k] = inv[k] ^ temp[k]

                    for i in range(4):
                        out = out + str(inv[i])
                    out = out + ' '

                    if pointer >= len(block) - 1:
                        continue

                print(out)

        else:  # CFB Mode
            bString = re.sub('[^01]', '', input('Please enter the m bit text blocks: '))
            kString = re.sub('[^01]', '', input('Please enter the 3 bit key: '))
            init = re.sub('[^01]', '', input('Please enter the initialization block: '))
            inverse = 1
            try:
                Round = int(input('Please enter the number of rounds: '))
                m = int(input('Please enter m: '))
            except ValueError:
                logger.error('Rounds and m must be integers.')
                return

            if len(kString) != 3:
                logger.error('Key must be exactly 3 bits, got %d.', len(kString))
                return
            if len(init) != 4:
                logger.error('Initialization block must be 4 bits, got %d.', len(init))
                return
            if m <= 0 or m > 4:
                logger.error('m must be between 1 and 4, got %d.', m)
                return
            if len(bString) == 0 or len(bString) % m != 0:
                logger.error('Block length %d must be a non-zero multiple of m=%d.', len(bString), m)
                return

            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)
            I = bc.convertStringList(init)
            logger.debug('CFB mode: key=%s, rounds=%d, m=%d', kString, Round, m)

            F = I
            for i in range(Round):
                F = bc.compute(F, key, inverse)
                if not F:
                    logger.error('CFB initialization failed.')
                    return

            L = [F[i] for i in range(m)]
            x = [block[i] for i in range(m)]
            y = [x[i] ^ L[i] for i in range(m)]
            out = str(y)
            pointer = m

            z = [F[i] for i in range(m, len(F))] + y[:]

            for i in range(m, len(block), m):
                F = z
                for j in range(Round):
                    F = bc.compute(F, key, inverse)

                for k in range(m):
                    L[k] = F[k]

                for i in range(m):
                    x[i] = block[pointer]
                    pointer += 1

                for i in range(m):
                    y[i] = (x[i] ^ L[i])

                out = out + str(y)

                for i in range(len(F)):
                    if i < m:
                        continue
                    else:
                        z[i - m] = F[i]

                for i in range(m):
                    z[i + m] = y[i]

            print(out)


if __name__ == "__main__":
    blockCyphers().run()
