# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# http://inventwithpython.com/hacking (BSD Licensed)
import sys
import re

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    # This text can be copy/pasted from http://invpy.com/vigenereCipher.py
    myFile = input ("Enter name of file that holds the message: ")
    myKey = input("Please enter the key: ")
    myMode = input("Please enter the mode (encrypt or decrypt): ") # set to 'encrypt' or 'decrypt'
    ctext = ''

    try:
        with open(myFile, 'r') as f:
            text = f.read()
            ctext = ctext + text

    except IOError as e:
        print('Error opening %s'%myFile)

    myMessage = re.sub('[^A-Z]','',ctext.upper())

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('%sed message:' % (myMode.title()))
    print(translated)
    
    try:
        fOut =open("vigenereOut.txt", 'w')
        fOut.write(translated)
        fOut.close()

    except IOError as e:
        print('Error writing to vigenereOut.txt')



def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = [] # stores the encrypted/decrypted message string

    keyIndex = 0
    key = key.upper()

    for symbol in message: # loop through each character in message
        num = LETTERS.find(symbol.upper())
        #print(num)
        if num != -1: # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                #print(LETTERS.find(key[keyIndex]))
                num += LETTERS.find(key[keyIndex]) # add if encrypting
                #print(num)
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # subtract if decrypting

            num %= len(LETTERS) # handle the potential wrap-around

            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # The symbol was not in LETTERS, so add it to translated as is.
            translated.append(symbol)

    return ''.join(translated)


# If vigenereCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()