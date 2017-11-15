import math

#Checks if the passed integer is prime
def isPrime(num):

    for i in range(2,math.ceil(math.sqrt(num)) + 1):
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
#Finds the max number to check up to based on the the highest number that will be a factor is the sqrt of the number
ceiling = math.ceil(math.sqrt(num)) 
#print('ceiling is %d'%ceiling)

#Count up to the ceiling
while count < ceiling + 1:
    if isPrime(count): #If the number is prime check to see if it is a factor

        if num%count == 0: #If count is a factor
            factor = count
            remainder = int(num/count)
            #print('factor = %d remainder = %d'%(factor,remainder))
            num = remainder
            ceiling = math.ceil(math.sqrt(num))
            output.append(factor)
            count = 2 #start the count over again

        else:
            count += 1 #if not, increase the count

    else:
        count += 1
            

if len(output) == 0: #if nothing has been appended to the list, the number is prime
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


