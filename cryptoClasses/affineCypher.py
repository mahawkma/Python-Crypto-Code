import sys
import logging
from subprocess import run

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#Class for the Affine Cypher. Please note that this code is using system calls for Unix.

class AffineCypher:
    #Function:     encryptAffine
    #Parameters:    string
    #Return:        None
    #Description: Function to encrypt a string with the Affine Cypher.
    def encryptAffine(self, fileName):
        print('y = (ax + b) mod 26')

        try:
            a = int(input('Please enter a: '))
            b = int(input('Please enter b: '))
        except ValueError:
            logger.error('Invalid input: a and b must be integers.')
            return

        logger.debug('Encrypting file "%s" with a=%d, b=%d', fileName, a, b)

        try:
            with open(fileName) as file, open('affineOut.txt', 'w') as out:
                for line in file:
                    line = line.upper()
                    cText = ''
                    for ch in line: #For each char in the line, if it is an alpha, convert to its ASCII int equivalent based on A = 0,
                                    #encrypt it, convert the int back to ASCII where A = 65, and then write it to the output string.
                        if ch.isalpha():
                            ch = ord(ch) - 65
                            ch = (a*ch + b)%26
                            cText = cText + chr(ch + 65)
                        else:
                            cText = cText + ch
                    out.write(cText)
        except FileNotFoundError:
            logger.error('Input file not found: %s', fileName)
            return
        except IOError as e:
            logger.error('File I/O error: %s', e)
            return

        logger.info('Encryption complete. Output written to affineOut.txt.')
        print('Output written to affineOut.txt:')
        run(['cat', 'affineOut.txt'])

    #Function:          decryptAffine
    #Parameters:        string
    #Return:            none
    #Descrption:       Function to decrypt an Affine Cypher with knowns
    def decryptAffine(self, fileName):
        dic = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25} #Dictionary with relative primes for a and 26
        print('x = a^-1 (y - b) mod 26')

        try:
            a = int(input('Please enter a: '))
            b = int(input('Please enter b: '))
        except ValueError:
            logger.error('Invalid input: a and b must be integers.')
            return

        if a not in dic:
            logger.error('Invalid value for a: %d. Must be coprime with 26 (valid values: %s)', a, sorted(dic.keys()))
            return

        aInverse = dic[a] #Modular inverse of a
        logger.debug('Decrypting file "%s" with a=%d, b=%d, a_inverse=%d', fileName, a, b, aInverse)

        try:
            with open(fileName) as file, open('affineDecrypt.txt', 'w') as out: #Similiar to the excrypt function above
                for line in file:
                    line = line.upper()
                    cText = ''
                    for ch in line:
                        if ch.isalpha():
                            ch = ord(ch) - 65
                            ch = aInverse*(ch - b)%26
                            cText = cText + chr(ch + 65)
                        else:
                            cText = cText + ch
                    out.write(cText)
        except FileNotFoundError:
            logger.error('Input file not found: %s', fileName)
            return
        except IOError as e:
            logger.error('File I/O error: %s', e)
            return

        logger.info('Decryption complete. Output written to affineDecrypt.txt.')
        print('Output written to affineDecrypt.txt:')
        run(['cat', 'affineDecrypt.txt'])


    def run(self):
        affine = AffineCypher()
        fileName = input('Please enter the filename of the text: ')
        choice = input("Please enter 1 for encrypt or 2 for decrypt: ")

        if choice == '1':
            affine.encryptAffine(fileName)
        elif choice == '2':
            affine.decryptAffine(fileName)
        else:
            logger.error('Invalid choice: "%s". Enter 1 or 2.', choice)


if __name__ == "__main__":
    AffineCypher().run()
