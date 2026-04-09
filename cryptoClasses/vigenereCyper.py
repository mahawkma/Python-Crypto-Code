# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# http://inventwithpython.com/hacking (BSD Licensed)
import sys
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
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

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    else:
        translated = decryptMessage(myKey, myMessage)

    print('%sed message:' % myMode.title())
    print(translated)
    logger.info('Translation complete.')

    try:
        with open("vigenereOut.txt", 'w') as fOut:
            fOut.write(translated)
        logger.info('Output written to vigenereOut.txt')
    except IOError as e:
        logger.error('Error writing to vigenereOut.txt: %s', e)


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = []
    keyIndex = 0
    key = key.upper()

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


if __name__ == '__main__':
    main()
