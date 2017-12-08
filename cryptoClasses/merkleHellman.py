import sys, re

class merkleHellman:

    #Given a number and a modulus, will return the inverse of that pair if they are relatively prime
    def inverseMod(self, a, m):
        for i in range(1,m):
            if ( m*i + 1) % a == 0:
                return ( m*i + 1) // a

    #Determines is a sequence is super increasing. If it is it returns True else it returns False
    def superIncreasing(self, nums):
        sum = 0

        for i in range(0, len(nums)):
            if nums[i] > sum:
                sum = sum + nums[i]
            else:
                return False

        return True

    #Create the public key given the sequence, prime, and multiple
    def publicKey(self, nums, prime, mult):
        out = []

        for x in range(0, len(nums)):
            out.append((mult*nums[x])%prime)

        return out

    #Decrypt the numerical message given the message, the sequence, the prime, and the multiple
    def decryptMH(self, decode, nums, prime, mult):

        mh = merkleHellman()
        inverse = mh.inverseMod(mult, prime) #Determine the inverse
        out = [0]*len(nums) #Create the output list with the appropriate size
        #print('Inverse = %d'%inverse)
        message = (inverse*decode)%prime #Decode the numerical message
        #print('Inverse message: %d'%message)

        for x in range(len(nums) - 1, -1, -1): #Go through the sequence backwards
            #print('For this loop x = %d and seq = %d'%(x, nums[x]))

            if nums[x] <= message: '''If the seq number at this position is equal to or less than the message, 
                                    write to output and reduce the message by the seq number'''
            out[x] = 1
            message = message - nums[x]

            else: #If the seq number is larger, do nothing
                out[x] = 0

            #print('message = %d'%message)

            if message == 0: #break out of the loop once the message has been finished being decoded
                break

        return out


    def run(self):

        mh = merkleHellman()
        """numbers = input('Please enter the sequence: ')
        numbers = numbers + ' '
        temp = ''
        nums = []
        sum = 0

        for ch in numbers:
            if ch == ' ':
               nums.append(int(temp)) 
               temp = ''
            else:
                temp = temp + ch

        print('Number list = ' + str(nums))

        if mh.superIncreasing(nums):
            print("Sequence is super increasing")
        else:
            print("Sequence is not super increasing")

        binary = input('Please enter the binary sequence: ')
        binList= []

        for ch in binary:
            binList.append(int(ch))

        print('binary list: ' + str(binList))

        if len(binList) != len(nums):
            print('Unable to encode.')
            exit(1)

        for x in range(0, len(nums)):
            if binList[x] == 1:
                sum = sum + nums[x]

        print('Encoded value: %d'%sum)"""

        seq = input('Please enter sequence for public key creation: ')
        prime = int(input('Please enter the prime value: '))
        mult = int(input('Please enter the multiple: '))
        seq = seq + ' '
        temp = ''
        nums = []
        key = []

        for ch in seq:
            if ch == ' ':
               nums.append(int(temp)) 
               temp = ''
            else:
                temp = temp + ch

        key = mh.publicKey(nums, prime, mult)

        print('Public Key = ' + str(key))
        print('Inverse mod = %d'%mh.inverseMod(mult,prime))

        decode = int(input('Please enter the number to decode: '))

        print('Decode value = ' + str(mh.decryptMH(decode, nums, prime, mult)))

if __name__ == "__main__":
    merkleHellman().run()