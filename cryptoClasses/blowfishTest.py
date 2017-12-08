
import blowfish
from operator import xor
import os

key = b'This is a test key'
cipher = blowfish.Cipher(key)

print('The test key is %s'%key)

print ("\nTesting block encrypt:")
text = b'testtest'
print ("\tText:\t\t%s" %text)
crypted = cipher.encrypt_block(text)
print ("\tEncrypted:\t%s" %crypted)
decrypted = cipher.decrypt_block(crypted)
print ("\tDecrypted:\t%s" %decrypted)
    
print ("\nTesting CTR encrypt:")
text = b"The quick brown fox jumps over the lazy dog"
print("\tText:\t\t", text)

# increment by one counters
nonce = int.from_bytes(os.urandom(8), "big")
enc_counter = blowfish.ctr_counter(nonce, f = xor)
dec_counter = blowfish.ctr_counter(nonce, f = xor)

crypted = b''.join(cipher.encrypt_ctr(text, enc_counter))
print ("\tEncrypted:\t%s"%crypted)

decrypted = b''.join(cipher.decrypt_ctr(crypted, dec_counter))
print ("\tDecrypted:\t", decrypted)

print ("\nTesting CBC encrypt:")

text = b"The quick brown fox jumps over the lazy dogXXXXX"
print ("\tText:\t\t", text)
iv = os.urandom(8) # initialization vector
print('\tInit Vector = %s'%str(iv))
crypted = b''.join(cipher.encrypt_cbc(text, iv))
print ("\tEncrypted:\t", crypted)
decrypted = b''.join(cipher.decrypt_cbc(crypted, iv))
print ("\tDecrypted:\t", decrypted)

print ("\nTesting speed")
from time import time
t1 = time()
n = 0
tlen = 0

while True:
    for i in range(1000):
        tstr = b"The quick brown fox jumps over the lazy dog %d" % i
        enc = cipher.encrypt_ctr(tstr, enc_counter)
        tlen += len(tstr)
    n += 1000
    t2 = time()
    if t2 - t1 > 5:
        break
t = t2 - t1
print ("%d encryptions in %0.1f seconds: %0.1f enc/s, %0.1f bytes/s" % (n, t, n / t, tlen / t))

