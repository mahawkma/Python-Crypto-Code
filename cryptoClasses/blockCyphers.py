import sys, re


class blockCyphers:

    dicS = {'000':'11', '001':'01', '010 ': '00', '011':'10', '100':'01', '101':'00', '110':'11', '111':'10'}

    #Convert binary text to an list of integers.
    def convertStringList(self, text):

        binaryList = []

        for ch in text:
            binaryList.append(int(ch))

        return binaryList

    #Calculate the t values for the computation using the block, its key, and the inverse value
    def tValues(self, block, key, inverse):

        bc = blockCyphers()
        dicS = {'000':'11', '001':'01', '010': '00', '011':'10', '100':'01', '101':'00', '110':'11', '111':'10'}
        t = []
        S = []
        stringS = ''
        stringT = ''

        if inverse == 1:
            S.append(block[2] ^ key[0])
            S.append(block[3] ^ key[1])
            S.append(block[2] ^ key[2])

        else:
            S.append(block[0] ^ key[0])
            S.append(block[1] ^ key[1])
            S.append(block[0] ^ key[2])

        #print('S = ' + str(S))

        for i in range(len(S)):
            stringS = stringS + str(S[i])

        #print ('stringS = %s' %stringS)

        stringT = dicS[stringS]

        t = bc.convertStringList(stringT)

        return t

    #Calculate the u values given the blockm the t values, and the inverse value
    def uValues(self, block, t, inverse):

        u = []

        if inverse == 1:
            u.append(block[0] ^ t[0])
            u.append(block[1] ^ t[1])
        else:
            u.append(block[2] ^ t[0])
            u.append(block[3] ^ t[1])

        return u

    #Compute the encryped or decrypted message given the block, the key, and the inverse value
    def compute(self, block, key, inverse):

        E = []
        D = []
        bc = blockCyphers()

        t = bc.tValues(block, key, inverse)
        #print('t = ' + str(t))

        u = bc.uValues(block, t, inverse)
        #print('u = ' + str(u))

        if inverse == 1:
            E.append(block[2])
            E.append(block[3])
            E.append(u[0])
            E.append(u[1])

            return E

        else:
            D.append(u[0])
            D.append(u[1])
            D.append(block[0])
            D.append(block[1])

            return D

    def run(self):
        mode = int(input('Please enter 1 for block mode, 2 for CBC mode, & 3 for CFB mode: '))
        bc = blockCyphers()

        if mode == 1: #Block Mode
            bString = input('Please enter 4 bit block: ')
            kString = input('Please enter the 3 bit key: ')
            Round = int(input('Please enther the number of rounds: '))
            inverse = int(input('Please enter 1 for non-inverse and 0 for inverse: '))
            block = []
            key = []
            returnBlock = ''

            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)

            for i in range(Round):
                #print('block = ' + str(block))
                #print('key = ' + str(key))
                block = bc.compute(block, key, inverse)
                #print('\n')

            print(block)

        elif mode == 2: #CBC Mode
            bString = input('Please enter input binary string: ')
            kString = input('Please enter the 3 bit key: ')
            inverse = int(input('Please enter 1 for non-inverse and 0 for inverse: '))
            Round = int(input('Please enther the number of rounds: '))
            block = []
            temp = [0,0,0,0]
            key = []
            y = []
            inv = []
            pointer = 0
            out = ''

            bString = re.sub('[^01]','', bString)
            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)

            while pointer < 4:
                y.append(block[pointer])
                pointer += 1

            #print('pointer = %d'%pointer)


            if inverse == 1:
                for i in range(int(len(block)/4)):
                    for i in range(Round):
                        #print('y = ' + str(y) + ' key = ' + str(key))
                        y = bc.compute(y, key, inverse)
                        #print(y)
                        #print('\n')

                    #print('y = ' + str(y))
                    for i in range(4):
                        out = out + str(y[i])

                    out = out + ' '

                    if pointer >= len(block) - 1:
                        continue

                    for j in range(4):
                        temp[j] = block[pointer]
                        #print('pointer = %d'%pointer)
                        pointer += 1

                    for k in range(4):
                        y[k] = y[k] ^ temp[k]

                print(out)

            else:

                for i in range(Round):
                        inv = bc.compute(y, key, inverse)

                for i in range(4):
                        out = out + str(inv[i])

                out = out + ' '


                for i in range(1, int(len(block)/4)):
                    for x in range(4):
                        temp[x] = y[x]
                    
                    for j in range(4):
                        y[j] = block[pointer]
                        #print('pointer = %d'%pointer)
                        pointer += 1

                    print('y = ' + str(y))

                    inv = y

                    for i in range(Round):
                        inv = bc.compute(inv, key, inverse)

                    #print('inverse = ' + str(inv))
                    #print('temp = ' + str(temp))

                    for k in range(4):
                        inv[k] = inv[k] ^ temp[k]

                    #print('x out = ' + str(inv))
                    #print('\n')


                    for i in range(4):
                        out = out + str(inv[i])

                    out = out + ' '

                    if pointer >= len(block) - 1:
                        continue

                print(out)

        else: #CFB Mode
            bString = input('Please enter input the m bit text blocks: ')
            kString = input('Please enter the 3 bit key: ')
            init = input('Please enter the initialization block: ')
            inverse = 1
            Round = int(input('Please enther the number of rounds: '))
            m = int(input('Please enter m: '))
            block = []
            temp = [0,0,0,0]
            key = []
            y = []
            x = []
            z = []
            F = []
            L = []
            pointer = 0
            out = ''

            bString = re.sub('[^01]','', bString)
            block = bc.convertStringList(bString)
            key = bc.convertStringList(kString)
            I = bc.convertStringList(init)

            F = I

            for i in range(Round):
                F = bc.compute(F, key, inverse)

            #print('F = ' + str(F))

            for i in range(0,m):
                L.append(F[i])

            #print('L = ' + str(L))

            for i in range(m):
                x.append(block[i])
                pointer += 1

            #print('x = ' + str(x))

            for i in range(m):
                y.append(x[i] ^ L[i])

            out = out + str(y)

            for i in range(len(F)):
                if i < m:
                    continue

                else:
                    z.append(F[i])

            for i in range(m):
                z.append(y[i])

            #print('z = ' + str(z))
            #print('\n')

            for i in range(m, len(block), m):
                F = z

                for j in range(Round):
                    F = bc.compute(F, key, inverse)

                for k in range(0,m):
                    L[k] = F[k]

                for i in range(m):
                    x[i] = block[pointer]
                    pointer += 1

                for i in range(m):
                    y[i] = (x[i] ^ L[i])

                out = out + str(y)

                for i in range(len(F)):
                    if i < m:
                        continue

                    else:
                        z[i-m] = F[i]

                    for i in range(m):
                        z[i + m] = y[i]

                #print('F = ' + str(F))
                #print('L = ' + str(L))
                #print('x = ' + str(x))
                #print('z = ' + str(z))
                #print('\n')

            print(out)


if __name__ == "__main__":
    blockCyphers().run()
