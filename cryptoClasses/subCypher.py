import sys
import math
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#Class to encrypt and decrypt substitution cyphers with a known key word

class subCypher:
    def run(self):
        sub = subCypher()

        kFile = input('Please enter the name of the file that contains the keyword: ')

        try:
            with open(kFile, 'r') as f:
                text = f.read().strip().upper().replace('\n', '').replace(' ', '')
        except FileNotFoundError:
            logger.error('Keyword file not found: %s', kFile)
            return
        except IOError as e:
            logger.error('Error reading keyword file %s: %s', kFile, e)
            return

        if not text:
            logger.error('Keyword file "%s" is empty.', kFile)
            return

        logger.debug('Keyword loaded from %s: %s', kFile, text)
        key = sub.createKey(text)
        if not key:
            return
        sub.encrypt(key)
        sub.decrypt(key)

    def createKey(self, keyWord):
        from string import ascii_uppercase

        kw = []
        usedCh = []

        for ch in keyWord:
            if ch.isalpha() and ch not in usedCh:
                kw.append(ch)
                usedCh.append(ch)

        if not kw:
            logger.error('Keyword contains no valid alphabetic characters.')
            return {}

        w = int(len(kw))
        print(w)
        h = int(math.ceil(26.0 / float(w)))
        print(h)
        kMatrix = [[' ' for x in range(0, w)] for y in range(0, h)]

        for x in range(0, w):
            kMatrix[0][x] = kw[x]

        for row_index, row in enumerate(kMatrix):
            for col_index, item in enumerate(row):
                if item != ' ':
                    continue
                else:
                    for ch in ascii_uppercase:
                        if ch in usedCh:
                            continue
                        else:
                            kMatrix[row_index][col_index] = ch
                            usedCh.append(ch)
                            break

        for row in kMatrix:
            text = ''
            for item in row:
                text = text + ' ' + str(item)
            print(text)

        key = {}
        r = 0
        c = 0

        for ch in ascii_uppercase:
            if (kMatrix[r][c] != ' '):
                key[ch] = kMatrix[r][c]
                if (r < h - 1):
                    r = r + 1
                else:
                    r = (r + 1) % h
                    c = c + 1
            else:
                r = (r + 1) % h
                c = c + 1
                key[ch] = kMatrix[r][c]
                r = r + 1

        logger.debug('Substitution key created successfully.')
        print(key)
        return key

    def encrypt(self, key):
        if not key:
            logger.error('Cannot encrypt: key is empty.')
            return

        fName = input('Please enter the name of the file that has the text to encrypt: ')
        eText = ''

        try:
            with open(fName, 'r') as f:
                text = f.read().upper()
                for ch in text:
                    if ch.isalpha():
                        eText = eText + key[ch]
                    else:
                        eText = eText + ch
        except FileNotFoundError:
            logger.error('Input file not found: %s', fName)
            return
        except IOError as e:
            logger.error('Error reading input file %s: %s', fName, e)
            return

        try:
            with open('encryptText.txt', 'w') as outFile:
                outFile.write(eText)
        except IOError as e:
            logger.error('Error writing to encryptText.txt: %s', e)
            return

        logger.info('Encryption complete. Output written to encryptText.txt')
        print(eText)
        print('Output written to encryptText.txt')

    def decrypt(self, key):
        if not key:
            logger.error('Cannot decrypt: key is empty.')
            return

        fName = input('Please enter the name of the file that has the text to decrypt: ')
        dText = ''
        iKey = {v: k for k, v in key.items()}

        try:
            with open(fName, 'r') as f:
                text = f.read().upper()
                for ch in text:
                    if ch.isalpha():
                        if ch not in iKey:
                            logger.warning('Character "%s" not found in inverse key, skipping.', ch)
                            continue
                        dText = dText + iKey[ch]
                    else:
                        dText = dText + ch
        except FileNotFoundError:
            logger.error('Input file not found: %s', fName)
            return
        except IOError as e:
            logger.error('Error reading input file %s: %s', fName, e)
            return

        try:
            with open('decryptText.txt', 'w') as outFile:
                outFile.write(dText)
        except IOError as e:
            logger.error('Error writing to decryptText.txt: %s', e)
            return

        logger.info('Decryption complete. Output written to decryptText.txt')
        print(dText)
        print('Output written to decryptText.txt')

if __name__ == "__main__":
    subCypher().run()
