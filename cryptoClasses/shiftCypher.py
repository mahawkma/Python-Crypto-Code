#include<stdio.h>
#include<stdlib.h>
import sys
import re

#Class for simple shift cyphers.
class ShiftCypher:

    #Function:      shiftCypher
    #Parameters:    string, int
    #Return:        string
    #Description:   Function to encrypt using a shift cypher.
    def shiftCypher(self, plaintext, shift):
        cText = ''
        #For loop that runs through every char in the string and encrypts is using the sift.
        for ch in plaintext:
            if ch.isalpha():
                ch = ord(ch) - 65 #Using A as 0 instead of 65
                ch = (ch + shift)%26
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
        c = ''
        dic = {}

        while place < len(text):
            c = text[place]
            #print('Place = %d: c = %s'%(place,c))
            cText = cText + c
            place = place + sets

        for x in ascii_uppercase:
            dic[x] = cText.count(x)

        return dic

    #Function:          indexC
    #Para:              dictionary
    #Return:            double
    #Description:       Takes a frequency count and returns the index of coincidence
    def indexC (self, dic, text):
        from string import ascii_uppercase
        eps = 0.000000
        dem = float(len(text)*(len(text) - 1))

        for ch in ascii_uppercase:
            eps = eps + dic[ch]*(dic[ch] - 1)

        #print('dem = %.6f eps = %.2f'%(dem,eps))
        return (eps/dem)

   #Function:           keyLength
   #Para:               double, string
   #Return:             double
   #Description:        Takes the incident of coincidence and the message lenght and returns the probable key length.
    def keyLength(self, I, message):
        n = len(message)

        k = float((.0265*n)/((.065 - I) + n*(I - .0385)))

        return k


    #Code to run the class if ran as main.
    def run(self):
        sft = ShiftCypher()
        fileName = raw_input('Please enter the filename of the text: ')
        sft.letterCounter(fileName)
        shift = int(raw_input('Please enter the cypher shift: '))

        with open(fileName) as file:
            for line in file:
                line = line.strip().upper()
                cypherText = sft.shiftCypher(line, shift)
                print(cypherText)



if __name__ == "__main__":
    ShiftCypher().run()
