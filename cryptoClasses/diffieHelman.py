import sys, re, math

sharedPrime = int(input("Please enter the shared prime: "))
sharedBase = int(input("Please enther shared base: "))
firstSecret = int(input("Please enter the first secret: "))
secondSecret = int(input("Please enther the second secret: "))

alpha = (sharedBase**firstSecret)%sharedPrime
beta = (sharedBase**secondSecret)%sharedPrime

kBeta = (beta**firstSecret)%sharedPrime
kAlpha = (alpha**secondSecret)%sharedPrime

print("alpha = %d beta = %d kBeta = %d kAlpha = %d"%(alpha, beta, kBeta, kAlpha))




