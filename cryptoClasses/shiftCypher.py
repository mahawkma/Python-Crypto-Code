#include<stdio.h>
#include<stdlib.h>
import sys
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#Class for simple shift cyphers.
class ShiftCypher:

    #Function:      shiftCypher
    #Parameters:    string, int
    #Return:        string
    #Description:   Function to encrypt using a shift cypher.
    def shiftCypher(self, plaintext, shift):
        cText = ''
        #For loop that runs through every char in the string and encrypts it using the shift.
        for ch in plaintext:
            if ch.isalpha():
                ch = ord(ch) - 65 #Using A as 0 instead of 65
                ch = (ch + shift) % 26
                cText = cText + chr(ch + 65) #Convert back to ASCII where A = 65
            else:
                cText = cText + ch
        return cText

    #Functions:         letterCounter
    #Parameters:        string, int, int
    #Return:            dictionary
    #Description:       Determines the frequency of characters in a string.
    def letterCounter(self, text, sets, place):
        from string import ascii_uppercase

        cText = ''
        dic = {}

        while place < len(text):
            cText = cText + text[place]
            place = place + sets

        for x in ascii_uppercase:
            dic[x] = cText.count(x)

        return dic

    #Function:          indexC
    #Para:              dictionary
    #Return:            double
    #Description:       Takes a frequency count and returns the index of coincidence
    def indexC(self, dic, text):
        from string import ascii_uppercase
        if len(text) <= 1:
            logger.error('indexC: text must have at least 2 characters.')
            return 0.0
        eps = 0.000000
        dem = float(len(text) * (len(text) - 1))

        for ch in ascii_uppercase:
            eps = eps + dic[ch] * (dic[ch] - 1)

        return (eps / dem)

   #Function:           keyLength
   #Para:               double, string
   #Return:             double
   #Description:        Takes the incident of coincidence and the message length and returns the probable key length.
    def keyLength(self, I, message):
        n = len(message)
        denom = (.065 - I) + n * (I - .0385)
        if denom == 0:
            logger.error('keyLength: denominator is zero, cannot compute key length.')
            return 0.0
        k = float((.0265 * n) / denom)
        return k

    #Code to run the class if ran as main.
    def run(self):
        sft = ShiftCypher()
        fileName = input('Please enter the filename of the text: ')

        try:
            shift = int(input('Please enter the cypher shift: '))
        except ValueError:
            logger.error('Shift must be an integer.')
            return

        logger.debug('Applying shift cipher: file=%s, shift=%d', fileName, shift)

        try:
            with open(fileName) as file:
                for line in file:
                    line = line.strip().upper()
                    cypherText = sft.shiftCypher(line, shift)
                    print(cypherText)
        except FileNotFoundError:
            logger.error('File not found: %s', fileName)
            return
        except IOError as e:
            logger.error('Error reading file %s: %s', fileName, e)
            return

        logger.info('Shift cipher complete.')


if __name__ == "__main__":
    ShiftCypher().run()
