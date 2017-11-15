import sys, re, math
from gcdEuclid import gcdEuclid

""" m = pq p and q are two prime integers
    n = (p -1)(q - 1)
    d = e^-1 mod n
    e = public key which must be relatively prime to pq"""

class RSA:

    def isPrime(self, num):

        for i in range(2,math.ceil(math.sqrt(num)) + 1):
            if (num % i) == 0:
                return False
    
        return True 

    def encrypt(self, message, e, m):
        num = message

        for i in range(0, e - 1):
            num = num*message

        return num%m

    def decrypt(self, message, d, m):
        num = message

        for i in range(0, d - 1):
            num = num*message

        return num%m

    def detD(self, e, n):
        gE = gcdEuclid()
        out = gE.ext_euclid(e, n)

        inverseE = out['t']

        return inverseE%n

    def detM(self, p, q):
        return p*q

    def detN(self, p, q):
        return (p - 1)*(q - 1)

    def charToInt (self, message):
        out = []

        for ch in message:
            out.append(ord(ch) - 65)

        return out


    def covertToBase(self, n, b):
        #print('Message = %d'%n)
        out = []

        if n == 0:
            return [0]

        while n:
            #print('n mod b = %d'%(n%b))
            out.append(n%b)
            n //= b

        return out[::-1]

    def numberBlock(self, block):
        out = 0

        for i in block:
            sum = sum + block[i]*math.pow(26,i)

        return sum

    def run(self):
        gE = gcdEuclid()
        rsa = RSA()

        while True:
            p = int(input('Please enter the first prime: '))
            if rsa.isPrime(p) == False:
                print('First number is not prime.')
                continue

            q = int(input('Please enter the second prime: '))
            if rsa.isPrime(q) == False:
                print('Second number is not prime.')
                continue

            e = int(input('Please input the public key:'))
            '''if (p * q)%e == 0:
                print('The public key is not relatively prime to pq.')
                continue'''

            break

        print('p = %d q = %d m = %d n = %d d = %d'%(p,q,rsa.detM(p,q), rsa.detN(p,q), rsa.detD(e,rsa.detN(p,q))))
        
        blockSize = int(input('Please enter the block size: '))
        decision = int(input("Enter 1 for encode or 2 for decode: "))
        message = input('Please enter the message: ')


        if decision == 1:
            message = re.sub('[^A-Z]','', message.upper())
            out = []
            text = rsa.charToInt(message)
            #print(text)
            sum = 0
            power = blockSize - 1

            for i in range(1, len(text) + 1):
                
                if i%blockSize == 0:
                    sum += text[i -1]*int(math.pow(26, power))
                    out.append(int(sum))
                    sum = 0
                    power = blockSize - 1

                else:
                    sum += text[i -1]*int(math.pow(26, power))
                    #print('Sum = %d'%sum)
                    power -= 1

            #out.append(int(sum))

            #print(out)

            for i in range(0, len(out)):
                out[i] = rsa.encrypt(out[i], e, rsa.detM(p,q))

            print('Output: ', end='')
            for i in range(0, len(out)):
                print(out[i], end=' ')

            print('')

        else:
            out = []
            text = []
            temp = ''

            for ch in message:
                if ch != ' ':
                    temp = temp + ch
                else:
                    text.append(int(temp))
                    temp = ''

            text.append(int(temp))

            for i in range(0, len(text)):
                text[i] = rsa.decrypt(text[i], rsa.detD(e,rsa.detN(p,q)), rsa.detM(p,q))

            #print(text)

            for i in range(0, len(text)):
                temp = rsa.covertToBase(text[i], 26)
                
                while len(temp)!= blockSize:
                    temp = [0] + temp

                #print(temp)

                for x in range(0,len(temp)):
                    out.append(temp[x])

            #print(out)

            for i in range(0, len(out)):
                print(chr(out[i] + 65), end = '')

            print('')

if __name__ == '__main__':
    RSA().run()
