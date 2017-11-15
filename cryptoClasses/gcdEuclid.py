import sys

class gcdEuclid:
    #Iteratiive Euclidian Algorithm
    def gcdIter(self, a, b):
        gE =gcdEuclid()

        if b == 0:
            return a
        else:
            return gE.gcdIter(b, a % b)

    #Extended Euclidian Alogorithm
    def ext_euclid(self, a,b):
        """Extended Euclid's algorithm for GCD.
        Given input a, b the function returns d such that gcd(a,b) = d
        and s, t such that as + bt = d, as well as u, v such that au = bv.""" 
        gE =gcdEuclid()
        
        if a < b:
            a, b = b, a 

        else:
            pass

        A = a
        B = b
        u, v, s, t = 0, 1, 1, 0 

        while b != 0:
            a, b, s, t, u, v = b, a % b, u, v, s - ( a // b ) * u, t - ( a // b ) * v 

        #return a, s, t, u, v

        out = {'a': a, 'b':b, 's':s, 't':t, 'u':u, 'v':v}

        #print('%d*%d + %d*%d = %d'%(A,s,B,t,gE.gcdIter(A,B)))

        return out


    def run(self):
        gE =gcdEuclid()

        a = int(input('Please enter first integer: '))
        b = int(input('Please enter second integer: '))

        gcd = gE.gcdIter(a,b)

        print('gcd of %d and %d is %d.'%(a,b,gcd))

        gE.ext_euclid(a,b)

if __name__ == "__main__":
    gcdEuclid().run()