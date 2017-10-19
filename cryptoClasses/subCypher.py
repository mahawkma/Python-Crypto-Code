#include<stdio.h>
#include<stdlib.h>
import sys
import math

#Class to encrypt and decrypt substitution cyphers with a known key word

class subCypher:
    def run(self):  
        sub = subCypher()

        try:
            kFile = input('Please enther the name of the file that contains the keyword: ')

        except IOError as e:
            print('Error opening file.')

        keyWord = ''

        with open(kFile, 'r') as f:
            text = f.read().strip().upper().replace('\n', '')
            text = text.replace(' ', '')
            keyWord = keyWord + text


        #print(keyWord)
        key = sub.createKey(keyWord)
        sub.encrypt(key)
        sub.decrypt(key)

    def createKey(self, keyWord):
        from string import ascii_uppercase 

        kw = []
        usedCh = []

        for ch in keyWord:
            if ch in usedCh:
                continue
            else:
                kw.append(ch)
                usedCh.append(ch)

        #print(usedCh)
        w = int(len(kw))
        print(w)
        h = int(math.ceil(26.0/float(w)))
        print(h)
        kMatrix = [[' ' for x in range(0, w)] for y in range(0, h)]

        for x in range (0, w):
            kMatrix[0][x] = kw[x]

        for row_index, row in enumerate(kMatrix):
            for col_index, item in enumerate(row):
                if item != ' ':
                    #print(item)
                    continue
                else:
                    for ch in ascii_uppercase:
                        if ch in usedCh:
                            #print('In used')
                            continue
                        else:
                            #print(ch)
                            kMatrix[row_index][col_index] = ch
                            usedCh.append(ch)
                            break

        for row in kMatrix:
            text = ''
            for item in row:
                text = text + ' ' + str(item)
            print (text)

        key = {}
        r = 0
        c = 0

        for ch in ascii_uppercase:
            #print('Plain = %s r = %d c = %d cipher = %s'%(ch, r, c, kMatrix[r][c]))
            if (kMatrix[r][c] != ' '):
                key[ch] = kMatrix[r][c]
                if (r < h - 1):
                    r = r + 1
                else:
                    r = (r + 1)%h
                    c = c + 1

            else:
                r = (r + 1)%h
                c = c + 1
                key[ch] = kMatrix[r][c]
                r = r + 1

        print(key)
        return key

    def encrypt(self, key):
        fName = input('Please enter the name of the file that has the text to encrypt: ')
        eText = ''
        outFile = open('encryptText.txt', 'w')

        with open(fName, 'r') as f:
            text = f.read().upper()
            for ch in text:
                if ch.isalpha():
                    eText = eText + key[ch]
                else:
                    eText = eText + ch

        outFile.write(eText)
        outFile.close()
        print(eText)
        print('Output written to encryptText.txt')

    def decrypt(self, key):
        fName = input('Please enter the name of the file that has the text to decrypt: ')
        dText = ''
        outFile = open('decryptText.txt', 'w')
        iKey = {v: k for k, v in key.items()}

        with open(fName, 'r') as f:
            text = f.read().upper()
            for ch in text:
                if ch.isalpha():
                    dText = dText + iKey[ch]
                else:
                    dText = dText + ch

        outFile.write(dText)
        outFile.close()
        print(dText)
        print('Output written to decryptText.txt')
            
if __name__ == "__main__":
    subCypher().run()






    