import math

def isPrime(num):

    for i in range(2,math.ceil(math.sqrt(num))):
        if (num % i) == 0:
            return False
    
    return True    

num = int(input('Please enter the number for factorize: '))
original = num
factor = 0
remainder = 0
output = []
ceiling = 0
count = 2
ceiling = math.ceil(math.sqrt(num))

#print('ceiling is %d'%ceiling)

while count < ceiling + 1:
    if isPrime(count):
        if num%count == 0:
            factor = count
            remainder = int(num/count)
            #print('factor = %d remainder = %d'%(factor,remainder))
            num = remainder
            ceiling = math.ceil(math.sqrt(num))
            output.append(factor)
            count = 2

        else:
            count += 1

    else:
        count += 1
            

if len(output) == 0:
    print('%s is prime'%original)
    exit(0)

print ('Factors of %d: '%original, end='')

if remainder != 1:
        output.append(remainder)

output.sort()

for x in range(0, len(output)):
    if x < len(output):
        print('%d '%output[x], end='')

print('')


