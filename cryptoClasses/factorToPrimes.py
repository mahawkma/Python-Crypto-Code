import math
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def isPrime(num):
    if num < 2:
        return False
    for i in range(2, math.ceil(math.sqrt(num)) + 1):
        if (num % i) == 0:
            return False
    return True

try:
    num = int(input('Please enter the number to factorize: '))
except ValueError:
    logger.error('Input must be an integer.')
    exit(1)

if num < 2:
    logger.error('Input must be an integer greater than 1, got %d.', num)
    exit(1)

logger.debug('Factorizing %d', num)

original = num
factor = 0
remainder = 0
output = []
count = 2
ceiling = math.ceil(math.sqrt(num))

while count < ceiling + 1:
    if isPrime(count):
        if num % count == 0:
            factor = count
            remainder = int(num / count)
            num = remainder
            ceiling = math.ceil(math.sqrt(num))
            output.append(factor)
            count = 2
        else:
            count += 1
    else:
        count += 1

if len(output) == 0:
    logger.info('%d is prime', original)
    print('%s is prime' % original)
    exit(0)

if remainder != 1:
    output.append(remainder)

output.sort()

print('Factors of %d: ' % original, end='')
for x in range(0, len(output)):
    print('%d ' % output[x], end='')
print('')

logger.info('Factors of %d: %s', original, output)
