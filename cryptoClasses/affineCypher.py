#include<stdio.h>
#include<stdlib.h>
import sys

#Class for the Affine Cypher. Please note that this code is using system calls for Unix.

class AffineCypher:
    #Function:     encryptAffine
    #Parameters:    string
    #Return:        None
    #Description: Function to encrypt a string with the Affine Cypher.
    def encryptAffine(self, fileName):
        from subprocess import call
        out = open('affineOut.txt', 'w')
        print('y = (ax + b) mod 26')
        a = int(input('Please enter a: '))
        b = int(input('Please enter b: '))

        with open(fileName) as file:
            for line in file: #For each line in the text file:
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

        print('Output written to affineOut.txt:')
        out.close()
        call(['cat', 'affineOut.txt'])

    #Function:          decryptAffine
    #Parameters:        string
    #Return:            none
    #Descrption:       Function to decrypt an Affine Cypher with knowns
    def decryptAffine(self, fileName):
        from subprocess import call
        dic = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25} #Dictionary with relative primes for a and 26
        out = open('affineDecrypt.txt', 'w')
        print('x = a^-1 (y - b) mod 26')
        a = int(input('Please enter a: '))
        b = int(input('Please enter b: '))
        aInverse = int(dic[a]) #Modular inverse of a
        #print(aInverse)

        with open(fileName) as file: #Similiar to the excrypt function above
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
        print('Output written to affineDecrypt.txt:')
        out.close()
        call(['cat', 'affineDecrypt.txt'])


    def run(self):
        affine = AffineCypher()
        fileName = raw_input('Please enter the filename of the text: ')
        affine.encryptAffine(fileName)
        affine.decryptAffine('affineOut.txt')


if __name__ == "__main__":
    AffineCypher().run()
