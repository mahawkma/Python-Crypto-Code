import sys, re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class binaryCyphers:

    def binaryVigenere(self, key, text):
        if not key:
            logger.error('Key cannot be empty.')
            return ''
        if not re.match('^[01]+$', key):
            logger.error('Key must contain only binary digits (0 and 1).')
            return ''

        keyArray = []
        textArray = []
        outArray = []
        keyPlace = 0
        out = ''

        for ch in key:
            keyArray.append(int(ch))

        for ch in text:
            if ch == ' ':
                textArray.append(ch)
            elif ch in ('0', '1'):
                textArray.append(int(ch))
            else:
                logger.warning('Non-binary character "%s" in text ignored.', ch)

        lenKey = len(keyArray)
        logger.debug('Binary Vigenere: key length=%d, text length=%d', lenKey, len(textArray))

        for i in range(0, len(textArray)):
            if textArray[i] == ' ':
                continue
            else:
                outArray.append((textArray[i] + keyArray[keyPlace % lenKey]) % 2)
                keyPlace += 1

        for i in range(0, len(outArray)):
            if outArray[i] == ' ':
                out = out + ' '
            else:
                out = out + str(outArray[i])

        return out

    def convertCharBinary(self, text):
        if not text:
            logger.error('Input text is empty.')
            return ''
        logger.debug('Converting %d characters to binary', len(text))
        return ' '.join(bin(x)[2:].zfill(8) for x in text.encode('utf-8'))

    def convertBinaryChar(self, binary):
        if not binary:
            logger.error('Input binary string is empty.')
            return ''
        binary = re.sub('[^0-1]', '', binary)
        if len(binary) % 8 != 0:
            logger.warning('Binary string length %d is not a multiple of 8; trailing bits ignored.', len(binary))
            binary = binary[:len(binary) - len(binary) % 8]
        logger.debug('Converting binary string of length %d to characters', len(binary))
        return ''.join((chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)))

    def run(self):
        exit(0)

if __name__ == "__main__":
    binaryCyphers().run()
