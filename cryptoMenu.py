#One must be running Python 3 for this bad boy to work.
import sys, re
from cryptoClasses.shiftCypher import ShiftCypher
from cryptoClasses.affineCypher import AffineCypher
from cryptoClasses.subCypher import subCypher
from cryptoClasses.vigenereCypher import vigenereCypher
from sympy.crypto.crypto import encipher_hill, decipher_hill #sympy is not part of the default Python install. This needs to be installed with PIP3.
from sympy import Matrix, pprint


#Menu system for the Cyber Tool kit.
class Menu:
    #Initialize the choices dictionary. Each choice will map to an action that will be taken.
    def __init__(self):
        self.choices = {
            "1": self.shift,
            "2": self.affineEncrypt,
            "3": self.affineDecrypt,
            "4": self.letterCounter,
            "5": self.freqCounter,
            "6": self.decryptSub,
            "7": self.encryptSub,
            "8": self.calcKeywordLength,
            "9": self.calcKey,
            "10": self.encryptVigenere,
            "11": self.decryptVigenere,
            "12": self.encypherHill,
            "13": self.decypherHill,
            "14": self.bruteSub,
            "15": self.bruteHill,
            "16": self.quit
                }

    #Function:          displayMenu
    #Paramaters:        None
    #Return Value:      None
    #Description:       Prints the menu for the Cyber Toolkit.

    def displayMenu(self):
        print('''
Cypher Toolkit Menu

1. Shift Cypher                     7. Substitution Encrypt         13. Decypher Hill
2. Encrypt with an Affine Cypher    8. Calculate Keyword Length     14. Brute Sub Cypher
3. Decrypt with an Affine Cypher    9. Calculate Key for Vigenere   15. Brute Hill
4. Letter Counter                   10. Encrypt Vigenere            16. Quit
5. Frequency Counter                11. Decrypt Vigenere
6. Substitution Decrypt             12. Encypher Hill
''')
    
    #Function:          run
    #Para:              None
    #Return:            None
    #Description:       Dislpays the menu and asks for a choice. If the choice is valid, executes the action signified by that choice.
    def run(self):
        while True:
            self.displayMenu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)

            if action:
                action()

            else:
                print("\n%s is not a valid choice." %choice)

    #Brute Sub Cypher using ngrams

    def bruteSub(self):
        from pycipher import SimpleSubstitution as SimpleSub
        import random
        import re
        from cryptoClasses.ngram_score import ngram_score
        import cryptoClasses.detectEnglish

        ngram = input('Please enter the name of the ngram file to try: ')
        fitness = ngram_score(ngram) # load our quadgram statistics
        #print(fitness)
        file = input('Please enter the name of the encrypted text file to crack: ')
        ctext=''

        with open(file, 'r') as f:
            text = f.read()
            ctext = ctext + text

        ctext = re.sub('[^A-Z]','',ctext.upper())

        maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        maxscore = -99e9
        parentscore,parentkey = maxscore,maxkey[:]
        print ("Substitution Cipher solver, you may have to wait several iterations")
        print ("for the correct result. Press ctrl+c to return to menu.")
        # keep going until we are killed by the user
        try:
            i = 0
            while 1:
                i = i+1
                random.shuffle(parentkey)
                deciphered = SimpleSub(parentkey).decipher(ctext)
                parentscore = fitness.score(deciphered)
                count = 0
                while count < 1000:
                    a = random.randint(0,25)
                    b = random.randint(0,25)
                    child = parentkey[:]
                    # swap two characters in the child
                    child[a],child[b] = child[b],child[a]
                    deciphered = SimpleSub(child).decipher(ctext)
                    score = fitness.score(deciphered)
                    # if the child was better, replace the parent with it
                    if (score > parentscore):
                        parentscore = score
                        parentkey = child[:]
                        count = 0
                    count = count+1
                # keep track of best score seen so far
                if parentscore>maxscore:
                    maxscore,maxkey = parentscore,parentkey[:]
                    print ('\nbest score so far:',maxscore,'on iteration',i)
                    ss = SimpleSub(maxkey)
                    print ('    best key: '+''.join(maxkey))
                    print ('    plaintext: '+ss.decipher(ctext))

        except KeyboardInterrupt as e:
                            print('\nWe are done!')
                            Menu().run()


    #Encypher a message using the Hill Cypher
    def encypherHill(self):
        #key = input("Please enter the key in the format [ [a,b], [c,d] ]: ")
        numRows = int(input('Please enter the number of rows in the matrix: '))
        fName = input('Please enter the name of the text file to encypher: ')
        text = ''
        val = ''

        numValues = numRows * numRows

        line = input('Please enter the values of the matrix in order seperated by spaces with a space at the end: ')

        mat = []

        for ch in line:
            if ch != ' ':
                val = val + ch

            elif ch == ' ':
                #print(val)
                mat.append(int(val))
                val = ''

        mKey = Matrix(numRows, numRows, mat)

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        out = encipher_hill(text, mKey)

        print(out)

    #Brute Force 2 x 2 Hill
    def bruteHill(self):
        from cryptoClasses.ngram_score import ngram_score
        import cryptoClasses.detectEnglish

        fName = input('Please enter the name of the text file to decypher: ')
        outFile = open('bruteHillOut.txt', 'w')
        fitness = ngram_score('quadgrams.txt') #Fitness function dependent on ngrams
        out = ''
        maxscore = -99e9

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        print('Bruting solutions. . .')
        print("This will take awhile. If you don't want to wait and think you found a solution, hit ctrl+c. The output will be written to bruteHillOut.txt.")

        #This will run through all the possible combinations of a 2x2 matrix
        for a in range(0,26):
            for b in range(0,26):
                for c in range(0,26):
                    for d in range(0,26):
                        mKey = Matrix(2,2,[a,b,c,d])

                        try:
                            out = decipher_hill(text, mKey) #decipher the text based on the current matrix

                        except ValueError as e: #catch if the matrix does not have an inverse
                            continue

                        except KeyboardInterrupt as e:
                            print('\nOutput written to bruteHillOut.txt')
                            Menu().run()

                        score = fitness.score(out) #Determine how much like English the decrypt is

                        if score > maxscore: # If score greater then max, output the results
                            outFile.write(str(mKey))
                            outFile.write(out)
                            outFile.write('\n')
                            maxscore = score
                            pprint(mKey)
                            print('Score: %f Text: %s'%(score, out))

        outFile.close()
        print('Output written to bruteHillOut.txt')


    #Decrypt a message using the Hill Cypher
    def decypherHill(self):
        numRows = int(input('Please enter the number of rows in the matrix: '))
        fName = input('Please enter the name of the text file to encypher: ')
        text = ''
        val =''

        numValues = numRows * numRows

        line = input('Please enter the values of the matrix in order seperated by spaces with a space at the end: ')

        mat = []

        for ch in line:
            if ch != ' ':
                val = val + ch

            elif ch == ' ':
                #print(val)
                mat.append(int(val))
                val = ''

        mKey = Matrix(numRows, numRows, mat)

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        out = decipher_hill(text, mKey)

        print(out)

    #Encrypt a message with the Vigenere Cypher
    def encryptVigenere(self):
        vc = vigenereCypher()
        fName = input('Please enter the name of the text file: ')
        kWord = input('Please enter the keyword: ')
        text = ''

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        out = vc.encryptMessage(kWord, text)

        print(out)

    #Decrypt a message that has been encyphered with the Vigenere Cypher
    def decryptVigenere(self):
        vc = vigenereCypher()
        fName = input('Please enter the name of the text file: ')
        kWord = input('Please enter the keyword: ')
        text = ''

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        out = vc.decryptMessage(kWord, text)

        print(out)
    
    #Calculates the possible key of a Vigenere Cypher using the dot product and outputs a table showing the values         
    def calcKey(self):
        vc = vigenereCypher()
        fName = input('Please enter the name of the text file: ')
        length = int(input('Please enter the length of keyword: '))
        text = ''

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        vc.calcKey(text, length)

    #Calculate the keyword length of a Vigenere Cypher and outputs it
    def calcKeywordLength(self):
        vc = vigenereCypher()
        fName = input('Please enter text file to do the calculation on: ')
        length = int(input('Please enter maximum length of keyword: '))
        text = ''
        l = 1

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        while l in range(1, length + 1):
            V = vc.calcV(text, l, length)
            A = vc.calcA(V, l)

            for i in range(len(V)):
                print('V%d = %f '%(i + 1, V[i]), sep = ' ', end='')
            
            print('A%d = %f'%(l, A))

            l = l + 1


    #Executes a shift cypher and prints the result to standard IO and to a file. 
    def shift(self):
        sft = ShiftCypher()
        fileName = input('Please enter the filename of the text: ')
        out = open('shiftOut.txt', 'w')

        #try:
            #freq = sft.letterCounter(fileName) #Determines freq of the chars in the passed file.
            #print(freq)

        #except IOError as e:
            #print('File not found')
            #Menu().run()

        shift = int(input('Please enter the cypher shift: '))

        try:
            with open(fileName) as file:
                for line in file:
                    shifted = sft.shiftCypher(line, shift)
                    out.write(shifted)
                    print(shifted)

        except IOError as e:
            print('File %s not found' %fileName)
            Menu().run()

        print('Output written to shiftOut.txt')

    #Executes the Affine Encrypt method. See class for more detailed comments.
    def affineEncrypt(self):
        affine = AffineCypher()
        try:
            fileName = input('Please enter the filename of the text: ')

        except IOError as e:
            print('File %s not found' %fileName)
            Menu().run()

        affine.encryptAffine(fileName)

    #Executes the Affine Decrypt method. See class for more detailed comments.
    def affineDecrypt(self):
        affine = AffineCypher()
        try:
            fileName = input('Please enter the filename of the text: ')

        except IOError as e:
            print('File %s not found' %fileName)
            Menu().run()

        affine.decryptAffine(fileName)

    #Determines the frequency of letters in a text file
    def freqCounter(self):
        vc = vigenereCypher()
        fName = input('Please enter text file to do frequency count on: ')
        sets = int(input('Please enther the number alphabets in use: '))
        place = 0
        text = ''

        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        while place < sets:
            freq = vc.letterFrequency(text, sets, place)

            from string import ascii_uppercase

            print('Set %d: '%(place + 1))
            for c in ascii_uppercase:
                print('[%s : %f];'%(c, freq[c]), sep = ' ', end='')

            place += 1
            print('\n')

    #Executes the letter counter to determine count of chars in text based on number of alphabets. Also calcs Index of Coincidence and possible key length
    def letterCounter(self):
        vc = vigenereCypher()
        fName = input('Please enter text file to do the count on: ')
        sets = int(input('Please enther the number alphabets in use: '))
        place = 0
        text = ''
        
        try:
            with open(fName, 'r') as f:
                text = f.read().strip().upper()

        except IOError as e:
            print('Unable to open %s' %fName)
            Menu().run()

        text = re.sub('[^A-Z]','', text)

        while place < sets:
            freq = vc.letterCounter(text, sets, place)

            from string import ascii_uppercase

            print('Set %d: '%(place + 1))
            for c in ascii_uppercase:
                print('[%s : %d];'%(c, freq[c]), sep = ' ', end='')

            place += 1
            print('\n')

        freq = vc.letterCounter(text, 1, 0)
        print('For text as a whole: ')

        for c in ascii_uppercase:
                print('[%s : %d];'%(c, freq[c]), sep = ' ', end='')

        print('\n')

        I = float(vc.indexC(freq, text))
        print('Index of Coincidence = %.6f.'%I)
        print('Possible key word length = %.6f' %vc.keyLength(I, text))

    #Ecrypt a message using a keyword and a substitution cypher
    def encryptSub(self):
        sub = subCypher()
        
        keyword = input('Please enter the keyword: ')
        keyword = key.upper()

        key = sub.createKey(keyword)
        sub.encrypt(key)

    #Decrypt a message using a keyword and a substitution cypher
    def decryptSub(self):
        sub = subCypher()
    
        keyword= input('Please enter the keyword: ')

        key = sub.createKey(keyword)
        sub.decrypt(key)

    #Quits the toolkit
    def quit(self):
        print("\nThank you for using the toolkit today")
        sys.exit(0)


if __name__ == "__main__":
    print("Welcome to the Crypto Toolkit!\n")
    Menu().run()