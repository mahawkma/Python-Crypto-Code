import sys, re

class vigenereCypher:

    #Func:              rotate
    #Para:              list, int
    #Return:            list
    #Description:       Takes a list and shifts the values in it n places to the left.

    def rotate(self, l, n):
        temp = []
        for x in range(0,26):
            temp.append(l[(x + n)%26])
        return temp

    #Func:              calcKey
    #Para:              string, int
    #Return:            none
    #Description:       Takes a message and a keyword length and will calculate the dot products and output them into a table.

    def calcKey(self, text, length):
        from string import ascii_uppercase
        out = [[ 0.0 for x in range(length)] for y in range(26)]
        b = [.08167, .01492, .02782, .04253, .12702, .02228, .02015, .06094, .06966, .00153, .00772, .04025, .02406, .06749, .07507, .01929, .00095, .05987, .06327, .09056, .02758, .00978, .02360, .00150, .01974, .00074]
        vc = vigenereCypher()

        for j in range(0, length):
            freq = vc.letterFrequency(text, length, j) #Find the frequency of letters in the coset
            a = []

            for ch in ascii_uppercase:
                a.append(freq[ch])

            for i in range(0,26): #Calculating the dot product of the a vector into the b vector with the a vector rotated 26 times
                dot = 0.0
                rot = vc.rotate(a, i) #rotating a

                for x in range(0,26):
                    dot = dot + rot[x]*b[x]
                
                out[i][j] = dot

        for i in range(0, 26):
            print('Shift = %2d   Keyletter = %s  '%(i, chr(i + 65)), end='')
            for j in range(0, length):
                print('%1.4f     '%out[i][j], sep = '', end='')
            print('\n')


    #Func:                  calcV
    #Para:                  string, int, int
    #Return:                float
    #Description:           Calculate the V values to use to determine the area undernath the scrawl curve.

    def calcV(self, text, length, max):
        vc = vigenereCypher()
        place = 0
        Vs = [0] * max

        while place < length:
            sum1 = 0.0
            sum2 = 0.0

            freq = vc.letterFrequency(text, length, place)
            values = sorted(freq.values())

            i =13
            for i in range(13,26):
                #print('V%d V%d '%(values[i], values[i-1]))
                sum1 = float(sum1 + values[i] + values[i-1])
                #print('Sum = %f i = %d' %(sum1, i))
                #i = i + 1

            i = 1
            for i in range(1,13):
                sum2 = sum2 + values[i] + values[i-1]
                #i = i + 1

            Vs[place] = ((sum1 - sum2)/2)
            place = place + 1
            #print(place)

        return Vs

    #Func:                  calcA
    #Para:                  float, int
    #Return:                float
    #Description:           Returns the average area under the curve of the scrawl.

    def calcA(self, V, length):
        sum = 0.0

        for i in range(len(V)):
            sum = float(sum + V[i])

        return sum/length

    #Function:          letterFrequency
    #Parameters:        string, int, int
    #Return:            dictionary
    #Descritpion:       Calculates the frequency of the letters in the message by key length.

    def letterFrequency(self, text, length, place):
        from string import ascii_uppercase 

        cText = ''
        c = ''
        dic = {}


        while place < len(text):
            c = text[place]
            cText = cText + c
            place = place + length

        count = len(cText)

        for x in ascii_uppercase:
            dic[x] = (cText.count(x))/count

        return dic
        

    #Functions:         letterCounter
    #Parameters:        string, int, int
    #Return:            dictionary
    #Description:       Determines the count of characters in a string.

    def letterCounter(self, text, sets, place):
        from string import ascii_uppercase 

        cText = ''
        c = ''
        dic = {}

        while place < len(text):
            c = text[place]
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

    #Function:          encryptMessage
    #Para:              string, string
    #Return:            string
    #Description:       encrypt a message with the given key.

    def encryptMessage(self, key, message):
        vc = vigenereCypher()
        return vc.translateMessage(key, message, 'encrypt')

    #Func:              decryptMessage
    #Para:              strng, string
    #Return:            string
    #Description:       Decrypt the message using the given key.

    def decryptMessage(self, key, message):
        vc = vigenereCypher()
        return vc.translateMessage(key, message, 'decrypt')

    #Func:              translateMessage
    #Para:              string, string, string
    #Return:            string
    #Description:       Decrypt or encrypt a message using the given key

    def translateMessage(self, key, message, mode):
        translated = [] # stores the encrypted/decrypted message string

        keyIndex = 0
        key = key.upper()
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


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

    def run(self):
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

        vc = vigenereCypher()

        if myMode == 'encrypt':
            translated = vc.encryptMessage(myKey, myMessage)
        elif myMode == 'decrypt':
            translated = vc.decryptMessage(myKey, myMessage)

        print('%sed message:' % (myMode.title()))
        print(translated)
    
        try:
            fOut =open("vigenereOut.txt", 'w')
            fOut.write(translated)
            fOut.close()

        except IOError as e:
            print('Error writing to vigenereOut.txt')


# If vigenereCipher.py is run (instead of imported as a class) call
# the run() function.
if __name__ == '__main__':
    vigenereCypher().run()