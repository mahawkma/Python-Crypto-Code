import logging
import os
from time import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

xor = lambda x, y: x ^ y

try:
    import blowfish
except ImportError:
    logger.error('blowfish module not installed. Install it with: pip install blowfish')
    exit(1)

key = b'This is a test key'

if len(key) < 8 or len(key) > 56:
    logger.error('Key length %d is invalid. Must be between 8 and 56 bytes.', len(key))
    exit(1)

try:
    cipher = blowfish.Cipher(key)
except Exception as e:
    logger.error('Failed to initialize Blowfish cipher: %s', e)
    exit(1)

print('The test key is %s' % key)
logger.debug('Initialized Blowfish cipher with key of length %d bytes', len(key))

print("\nTesting block encrypt:")
text = b'testtest'
print("\tText:\t\t%s" % text)
try:
    crypted = cipher.encrypt_block(text)
    print("\tEncrypted:\t%s" % crypted)
    decrypted = cipher.decrypt_block(crypted)
    print("\tDecrypted:\t%s" % decrypted)
    if decrypted == text:
        logger.info('Block encrypt/decrypt: OK')
    else:
        logger.warning('Block encrypt/decrypt mismatch: original=%s, decrypted=%s', text, decrypted)
except Exception as e:
    logger.error('Block encrypt/decrypt failed: %s', e)

print("\nTesting CTR encrypt:")
text = b"The quick brown fox jumps over the lazy dog"
print("\tText:\t\t", text)

try:
    nonce = int.from_bytes(os.urandom(8), "big")
    enc_counter = blowfish.ctr_counter(nonce, f=xor)
    dec_counter = blowfish.ctr_counter(nonce, f=xor)

    crypted = b''.join(cipher.encrypt_ctr(text, enc_counter))
    print("\tEncrypted:\t%s" % crypted)

    decrypted = b''.join(cipher.decrypt_ctr(crypted, dec_counter))
    print("\tDecrypted:\t", decrypted)

    if decrypted == text:
        logger.info('CTR encrypt/decrypt: OK')
    else:
        logger.warning('CTR encrypt/decrypt mismatch!')
except Exception as e:
    logger.error('CTR encrypt/decrypt failed: %s', e)

print("\nTesting CBC encrypt:")
text = b"The quick brown fox jumps over the lazy dogXXXXX"
print("\tText:\t\t", text)

try:
    iv = os.urandom(8) # initialization vector
    print('\tInit Vector = %s' % str(iv))
    crypted = b''.join(cipher.encrypt_cbc(text, iv))
    print("\tEncrypted:\t", crypted)
    decrypted = b''.join(cipher.decrypt_cbc(crypted, iv))
    print("\tDecrypted:\t", decrypted)

    if decrypted == text:
        logger.info('CBC encrypt/decrypt: OK')
    else:
        logger.warning('CBC encrypt/decrypt mismatch!')
except Exception as e:
    logger.error('CBC encrypt/decrypt failed: %s', e)

print("\nTesting speed")
try:
    nonce = int.from_bytes(os.urandom(8), "big")
    enc_counter = blowfish.ctr_counter(nonce, f=xor)
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
    print("%d encryptions in %0.1f seconds: %0.1f enc/s, %0.1f bytes/s" % (n, t, n / t, tlen / t))
    logger.info('Speed test: %d encryptions in %.1f seconds (%.1f enc/s)', n, t, n / t)
except Exception as e:
    logger.error('Speed test failed: %s', e)
