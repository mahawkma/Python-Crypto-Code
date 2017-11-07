import sys

#Iteratiive Euclidian Algorithm
def gcdIter(a, b):
    if b == 0:
        return a
    else:
        return gcdIter(b, a % b)

#Extended Euclidian Alogorithm
def ext_euclid(a,b):
    """Extended Euclid's algorithm for GCD.
    Given input a, b the function returns d such that gcd(a,b) = d
    and s, t such that as + bt = d, as well as u, v such that au = bv.""" 

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

    print('%d*%d + %d*%d = %d'%(A,s,B,t,gcdIter(A,B)))


a = int(input('Please enter first integer: '))
b = int(input('Please enter second integer: '))

gcd = gcdIter(a,b)

print('gcd of %d and %d is %d.'%(a,b,gcd))

ext_euclid(a,b)