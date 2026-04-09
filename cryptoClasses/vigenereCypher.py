import sys, re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class vigenereCypher:

    #Func:              rotate
    #Para:              list, int
    #Return:            list
    #Description:       Takes a list and shifts the values in it n places to the left.

    def rotate(self, l, n):
        temp = []
        for x in range(0, 26):
            temp.append(l[(x + n) % 26])
        return temp

    #Func:              calcKey
    #Para:              string, int
    #Return:            none
    #Description:       Takes a message and a keyword length and calculates the dot products.

    def calcKey(self, text, length):
        from string import ascii_uppercase
        if length <= 0:
            logger.error('calcKey: key length must be a positive integer, got %d.', length)
            return
        out = [[0.0 for x in range(length)] for y in range(26)]
        b = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, .00153, .00772, .04025, .02406, .06749, .07507, .01929, .00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074]
        vc = vigenereCypher()

        logger.debug('Calculating key table for length %d', length)

        for j in range(0, length):
            freq = vc.letterFrequency(text, length, j)
            a = []
            for ch in ascii_uppercase:
                a.append(freq[ch])
            for i in range(0, 26):
                dot = 0.0
                rot = vc.rotate(a, i)
                for x in range(0, 26):
                    dot = dot + rot[x] * b[x]
                out[i][j] = dot

        for i in range(0, 26):
            print('Shift = %2d   Keyletter = %s  ' % (i, chr(i + 65)), end='')
            for j in range(0, length):
                print('%1.4f     ' % out[i][j], sep='', end='')
            print('\n')

    #Func:                  calcV
    #Para:                  string, int, int
    #Return:                float
    #Description:           Calculate the V values to determine area under the scrawl curve.

    def calcV(self, text, length, max):
        vc = vigenereCypher()
        place = 0
        Vs = [0] * max

        while place < length:
            sum1 = 0.0
            sum2 = 0.0
            freq = vc.letterFrequency(text, length, place)
            values = sorted(freq.values())
            for i in range(13, 26):
                sum1 = float(sum1 + values[i] + values[i - 1])
            for i in range(1, 13):
                sum2 = sum2 + values[i] + values[i - 1]
            Vs[place] = ((sum1 - sum2) / 2)
            place = place + 1

        return Vs

    #Func:                  calcA
    #Para:                  float, int
    #Return:                float
    #Description:           Returns the average area under the curve of the scrawl.

    def calcA(self, V, length):
        if length == 0:
            logger.error('calcA: length cannot be zero.')
            return 0.0
        total = 0.0
        for i in range(len(V)):
            total = float(total + V[i])
        return total / length

    #Function:          letterFrequency
    #Parameters:        string, int, int
    #Return:            dictionary
    #Description:       Calculates the frequency of letters in the message by key length.

    def letterFrequency(self, text, length, place):
        from string import ascii_uppercase
        if length == 0:
            logger.error('letterFrequency: length cannot be zero.')
            return {ch: 0.0 for ch in ascii_uppercase}
        cText = ''
        while place < len(text):
            cText = cText + text[place]
            place = place + length
        count = len(cText)
        if count == 0:
            logger.warning('letterFrequency: no characters found for this coset.')
            return {ch: 0.0 for ch in ascii_uppercase}
        dic = {}
        for x in ascii_uppercase:
            dic[x] = (cText.count(x)) / count
        return dic

    #Functions:         letterCounter
    #Parameters:        string, int, int
    #Return:            dictionary
    #Description:       Determines the count of characters in a string.

    def letterCounter(self, text, sets, place):
        from string import ascii_uppercase
        cText = ''
        while place < len(text):
            cText = cText + text[place]
            place = place + sets
        dic = {}
        for x in ascii_uppercase:
            dic[x] = cText.count(x)
        return dic

    #Function:          indexC
    #Para:              dictionary
    #Return:            double
    #Description:       Takes a frequency count and returns the index of coincidence.

    def indexC(self, dic, text):
        from string import ascii_uppercase
        if len(text) <= 1:
            logger.error('indexC: text must have at least 2 characters.')
            return 0.0
        eps = 0.0
        dem = float(len(text) * (len(text) - 1))
        for ch in ascii_uppercase:
            eps = eps + dic[ch] * (dic[ch] - 1)
        return (eps / dem)

    #Function:           keyLength
    #Para:               double, string
    #Return:             double
    #Description:        Takes the index of coincidence and message length and returns probable key length.

    def keyLength(self, I, message):
        n = len(message)
        denom = (.065 - I) + n * (I - .0385)
        if denom == 0:
            logger.error('keyLength: denominator is zero, cannot compute key length.')
            return 0.0
        k = float((.0265 * n) / denom)
        return k

    #Function:          encryptMessage
    #Para:              string, string
    #Return:            string
    #Description:       Encrypt a message with the given key.

    def encryptMessage(self, key, message):
        vc = vigenereCypher()
        return vc.translateMessage(key, message, 'encrypt')

    #Func:              decryptMessage
    #Para:              string, string
    #Return:            string
    #Description:       Decrypt the message using the given key.

    def decryptMessage(self, key, message):
        vc = vigenereCypher()
        return vc.translateMessage(key, message, 'decrypt')

    #Func:              translateMessage
    #Para:              string, string, string
    #Return:            string
    #Description:       Decrypt or encrypt a message using the given key.

    def translateMessage(self, key, message, mode):
        if not key:
            logger.error('translateMessage: key cannot be empty.')
            return ''
        translated = []
        keyIndex = 0
        key = key.upper()
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for symbol in message:
            num = LETTERS.find(symbol.upper())
            if num != -1:
                if mode == 'encrypt':
                    num += LETTERS.find(key[keyIndex])
                elif mode == 'decrypt':
                    num -= LETTERS.find(key[keyIndex])
                num %= len(LETTERS)
                if symbol.isupper():
                    translated.append(LETTERS[num])
                elif symbol.islower():
                    translated.append(LETTERS[num].lower())
                keyIndex += 1
                if keyIndex == len(key):
                    keyIndex = 0
            else:
                translated.append(symbol)

        return ''.join(translated)

    def run(self):
        myFile = input("Enter name of file that holds the message: ")
        myKey = input("Please enter the key: ")
        myMode = input("Please enter the mode (encrypt or decrypt): ")

        if not myKey:
            logger.error('Key cannot be empty.')
            return

        if myMode not in ('encrypt', 'decrypt'):
            logger.error('Invalid mode "%s". Must be "encrypt" or "decrypt".', myMode)
            return

        ctext = ''
        try:
            with open(myFile, 'r') as f:
                ctext = f.read()
        except FileNotFoundError:
            logger.error('File not found: %s', myFile)
            return
        except IOError as e:
            logger.error('Error opening %s: %s', myFile, e)
            return

        myMessage = re.sub('[^A-Z]', '', ctext.upper())

        if not myMessage:
            logger.error('File "%s" contains no alphabetic characters.', myFile)
            return

        logger.debug('Mode: %s, key: %s, message length: %d', myMode, myKey, len(myMessage))

        vc = vigenereCypher()
        if myMode == 'encrypt':
            translated = vc.encryptMessage(myKey, myMessage)
        else:
            translated = vc.decryptMessage(myKey, myMessage)

        print('%sed message:' % myMode.title())
        print(translated)
        logger.info('Translation complete.')

        try:
            with open("vigenereOut.txt", 'w') as fOut:
                fOut.write(translated)
            logger.info('Output written to vigenereOut.txt')
        except IOError as e:
            logger.error('Error writing to vigenereOut.txt: %s', e)


if __name__ == '__main__':
    vigenereCypher().run()
