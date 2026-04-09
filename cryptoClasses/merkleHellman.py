import sys, re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class merkleHellman:

    #Given a number and a modulus, will return the inverse of that pair if they are relatively prime
    def inverseMod(self, a, m):
        if a == 0:
            logger.error('inverseMod: a cannot be zero.')
            return None
        for i in range(1, m):
            if (m * i + 1) % a == 0:
                return (m * i + 1) // a
        logger.error('inverseMod: no modular inverse found for a=%d, m=%d.', a, m)
        return None

    #Determines if a sequence is super increasing. Returns True if so, else False.
    def superIncreasing(self, nums):
        total = 0
        for i in range(0, len(nums)):
            if nums[i] > total:
                total = total + nums[i]
            else:
                return False
        return True

    #Create the public key given the sequence, prime, and multiple
    def publicKey(self, nums, prime, mult):
        out = []
        for x in range(0, len(nums)):
            out.append((mult * nums[x]) % prime)
        return out

    #Decrypt the numerical message given the message, the sequence, the prime, and the multiple
    def decryptMH(self, decode, nums, prime, mult):
        mh = merkleHellman()
        inverse = mh.inverseMod(mult, prime)
        if inverse is None:
            logger.error('decryptMH: could not compute modular inverse.')
            return []
        out = [0] * len(nums)
        message = (inverse * decode) % prime
        logger.debug('decryptMH: inverse=%d, decoded message value=%d', inverse, message)

        for x in range(len(nums) - 1, -1, -1): #Go through the sequence backwards
            if nums[x] <= message: # If the seq number is <= message, write to output and reduce message
                out[x] = 1
                message = message - nums[x]

            else: #If the seq number is larger, do nothing
                out[x] = 0

            if message == 0: #break out of the loop once the message has been finished being decoded
                break

        return out

    def _parse_sequence(self, seq_str):
        """Parse a space-separated integer sequence string into a list of ints."""
        nums = []
        for token in seq_str.strip().split():
            try:
                nums.append(int(token))
            except ValueError:
                logger.error('Invalid value in sequence: "%s"', token)
                return None
        return nums

    def run(self):
        mh = merkleHellman()

        seq = input('Please enter sequence for public key creation: ')
        nums = self._parse_sequence(seq)
        if nums is None or len(nums) == 0:
            logger.error('Invalid or empty sequence.')
            return

        try:
            prime = int(input('Please enter the prime value: '))
            mult = int(input('Please enter the multiple: '))
        except ValueError:
            logger.error('Prime and multiple must be integers.')
            return

        if prime <= 0 or mult <= 0:
            logger.error('Prime and multiple must be positive integers.')
            return

        logger.debug('Creating public key: nums=%s, prime=%d, mult=%d', nums, prime, mult)

        key = mh.publicKey(nums, prime, mult)
        print('Public Key = ' + str(key))

        inv = mh.inverseMod(mult, prime)
        if inv is None:
            logger.error('Could not compute inverse mod. Check that mult and prime are coprime.')
            return
        print('Inverse mod = %d' % inv)

        try:
            decode = int(input('Please enter the number to decode: '))
        except ValueError:
            logger.error('Decode value must be an integer.')
            return

        result = mh.decryptMH(decode, nums, prime, mult)
        print('Decode value = ' + str(result))
        logger.info('Decryption complete: %s', result)

if __name__ == "__main__":
    merkleHellman().run()
