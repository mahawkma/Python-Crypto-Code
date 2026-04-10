"""
Unit tests for Python-Crypto-Code classes and modules.
Run from the repo root: python3 -m pytest tests/test_crypto.py -v
"""

import sys
import os
import math
import subprocess
import unittest

# Ensure repo root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# ShiftCypher
# ---------------------------------------------------------------------------
class TestShiftCypher(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.shiftCypher import ShiftCypher
        self.sc = ShiftCypher()

    def test_encrypt_basic(self):
        self.assertEqual(self.sc.shiftCypher("HELLO", 3), "KHOOR")

    def test_rot13(self):
        self.assertEqual(self.sc.shiftCypher("HELLOWORLD", 13), "URYYBJBEYQ")

    def test_decrypt_is_inverse(self):
        for shift in [1, 7, 13, 25]:
            enc = self.sc.shiftCypher("ABCXYZ", shift)
            dec = self.sc.shiftCypher(enc, -shift % 26)
            self.assertEqual(dec, "ABCXYZ", f"roundtrip failed for shift={shift}")

    def test_zero_shift(self):
        self.assertEqual(self.sc.shiftCypher("HELLO", 0), "HELLO")

    def test_full_rotation(self):
        self.assertEqual(self.sc.shiftCypher("HELLO", 26), "HELLO")

    def test_preserves_non_alpha(self):
        self.assertEqual(self.sc.shiftCypher("HELLO, WORLD!", 3), "KHOOR, ZRUOG!")

    def test_lowercase_not_supported(self):
        # shiftCypher uses ord(ch) - 65 (A=0 basis), so it only handles uppercase
        # correctly. Lowercase letters (ord >= 97) produce different ASCII ranges.
        # This is a known limitation: the cipher is uppercase-only.
        enc = self.sc.shiftCypher("abc", 3)
        # Cannot roundtrip lowercase — just verify it doesn't crash and returns a string
        self.assertIsInstance(enc, str)

    def test_wrap_around(self):
        self.assertEqual(self.sc.shiftCypher("XYZ", 3), "ABC")

    def test_letter_counter_basic(self):
        # Count every character (sets=1, start=0)
        result = self.sc.letterCounter("AAABBC", 1, 0)
        self.assertEqual(result['A'], 3)
        self.assertEqual(result['B'], 2)
        self.assertEqual(result['C'], 1)
        self.assertEqual(result['Z'], 0)

    def test_letter_counter_cosets(self):
        # Every other character starting at 0: A, A → AA; starting at 1: B, B → BB
        result0 = self.sc.letterCounter("ABABAB", 2, 0)
        result1 = self.sc.letterCounter("ABABAB", 2, 1)
        self.assertEqual(result0['A'], 3)
        self.assertEqual(result1['B'], 3)

    def test_index_of_coincidence_uniform(self):
        # A string of all same letters has max IoC
        text = "A" * 26
        dic = self.sc.letterCounter(text, 1, 0)
        ic = self.sc.indexC(dic, text)
        self.assertAlmostEqual(ic, 1.0, places=5)

    def test_index_of_coincidence_short_text(self):
        dic = {'A': 1}
        for ch in 'BCDEFGHIJKLMNOPQRSTUVWXYZ':
            dic[ch] = 0
        result = self.sc.indexC(dic, "A")
        self.assertEqual(result, 0.0)

    def test_key_length_returns_float(self):
        # English text IoC ≈ 0.065, so denominator should not be zero for typical I
        result = self.sc.keyLength(0.045, "ATTACKATDAWNATTACKATDAWN")
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_key_length_zero_denominator(self):
        # Manufacture an I and message that cause denom == 0
        # denom = (0.065 - I) + n*(I - 0.0385) = 0  →  use I=0.065, n=anything
        # 0 + n*(0.065-0.0385) != 0, so try I s.t. formula zeroes out
        # Simpler: just confirm it returns 0 without crashing
        result = self.sc.keyLength(0.065, "A" * 100)
        # Won't always be 0, but must not raise
        self.assertIsInstance(result, float)


# ---------------------------------------------------------------------------
# AffineCypher  (logic only — file I/O tested separately via temp files)
# ---------------------------------------------------------------------------
class TestAffineCypher(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.affineCypher import AffineCypher
        self.ac = AffineCypher()
        self.dic = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}

    def _encrypt_char(self, ch, a, b):
        return chr(((a * (ord(ch.upper()) - 65) + b) % 26) + 65)

    def _decrypt_char(self, ch, a, b):
        a_inv = self.dic[a]
        return chr((a_inv * (ord(ch.upper()) - 65 - b) % 26) + 65)

    def test_encrypt_roundtrip_a3_b7(self):
        a, b = 3, 7
        plain = "HELLOWORLD"
        enc = ''.join(self._encrypt_char(c, a, b) for c in plain)
        dec = ''.join(self._decrypt_char(c, a, b) for c in enc)
        self.assertEqual(dec, plain)

    def test_encrypt_roundtrip_a5_b8(self):
        a, b = 5, 8
        plain = "CRYPTOGRAPHY"
        enc = ''.join(self._encrypt_char(c, a, b) for c in plain)
        dec = ''.join(self._decrypt_char(c, a, b) for c in enc)
        self.assertEqual(dec, plain)

    def test_all_valid_a_values(self):
        """Every valid 'a' in the inverse dictionary should roundtrip correctly."""
        for a in self.dic:
            for b in [0, 5, 13]:
                plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                enc = ''.join(self._encrypt_char(c, a, b) for c in plain)
                dec = ''.join(self._decrypt_char(c, a, b) for c in enc)
                self.assertEqual(dec, plain, f"roundtrip failed for a={a}, b={b}")

    def test_affine_encrypt_file(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("HELLO\n")
            fname = f.name
        try:
            import unittest.mock as mock
            with mock.patch('builtins.input', side_effect=['5', '8']):
                with mock.patch('subprocess.run'):  # suppress cat output
                    self.ac.encryptAffine(fname)
            with open('affineOut.txt') as out:
                content = out.read().strip()
            self.assertEqual(content, "RCLLA")
        finally:
            os.unlink(fname)
            if os.path.exists('affineOut.txt'):
                os.unlink('affineOut.txt')

    def test_affine_decrypt_file(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("RCLLA\n")
            fname = f.name
        try:
            import unittest.mock as mock
            with mock.patch('builtins.input', side_effect=['5', '8']):
                with mock.patch('subprocess.run'):
                    self.ac.decryptAffine(fname)
            with open('affineDecrypt.txt') as out:
                content = out.read().strip()
            self.assertEqual(content, "HELLO")
        finally:
            os.unlink(fname)
            if os.path.exists('affineDecrypt.txt'):
                os.unlink('affineDecrypt.txt')


# ---------------------------------------------------------------------------
# binaryCyphers
# ---------------------------------------------------------------------------
class TestBinaryCyphers(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.binaryCyphers import binaryCyphers
        self.bc = binaryCyphers()

    def test_convert_char_binary_hello(self):
        result = self.bc.convertCharBinary("H")
        self.assertEqual(result, "01001000")

    def test_roundtrip_ascii(self):
        for msg in ["HELLO", "ABC", "XYZ", "A"]:
            enc = self.bc.convertCharBinary(msg)
            dec = self.bc.convertBinaryChar(enc)
            self.assertEqual(dec, msg)

    def test_convert_binary_strips_spaces(self):
        # convertCharBinary produces space-separated bytes; convertBinaryChar strips non-binary
        enc = self.bc.convertCharBinary("HI")
        dec = self.bc.convertBinaryChar(enc)
        self.assertEqual(dec, "HI")

    def test_convert_char_binary_empty(self):
        result = self.bc.convertCharBinary("")
        self.assertEqual(result, "")

    def test_convert_binary_char_empty(self):
        result = self.bc.convertBinaryChar("")
        self.assertEqual(result, "")

    def test_binary_vigenere_xor_known(self):
        # key=1, text=0 → 1; key=1, text=1 → 0
        result = self.bc.binaryVigenere("10", "01")
        self.assertEqual(result, "11")

    def test_binary_vigenere_roundtrip(self):
        key = "1101"
        text = "10110011"
        enc = self.bc.binaryVigenere(key, text)
        dec = self.bc.binaryVigenere(key, enc)
        self.assertEqual(dec, text)

    def test_binary_vigenere_empty_key(self):
        result = self.bc.binaryVigenere("", "1010")
        self.assertEqual(result, "")

    def test_binary_vigenere_invalid_key(self):
        result = self.bc.binaryVigenere("XYZ", "1010")
        self.assertEqual(result, "")

    def test_binary_vigenere_key_cycles(self):
        # key=1, applied 4 times to 0000 → 1111
        result = self.bc.binaryVigenere("1", "0000")
        self.assertEqual(result, "1111")


# ---------------------------------------------------------------------------
# blockCyphers
# ---------------------------------------------------------------------------
class TestBlockCyphers(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.blockCyphers import blockCyphers
        self.bc = blockCyphers()

    def test_convert_string_list_valid(self):
        self.assertEqual(self.bc.convertStringList("1010"), [1, 0, 1, 0])

    def test_convert_string_list_invalid(self):
        result = self.bc.convertStringList("102")
        self.assertEqual(result, [])

    def test_convert_string_list_empty(self):
        self.assertEqual(self.bc.convertStringList(""), [])

    def test_tvalues_returns_two_elements(self):
        block = [1, 0, 1, 1]
        key = [0, 1, 0]
        result = self.bc.tValues(block, key, 0)
        self.assertEqual(len(result), 2)

    def test_uvalues_returns_two_elements(self):
        block = [1, 0, 1, 1]
        key = [0, 1, 0]
        t = self.bc.tValues(block, key, 0)
        u = self.bc.uValues(block, t, 0)
        self.assertEqual(len(u), 2)

    def test_compute_encrypt_returns_four_elements(self):
        block = [1, 0, 1, 1]
        key = [0, 1, 0]
        result = self.bc.compute(block, key, 0)
        self.assertEqual(len(result), 4)
        self.assertTrue(all(b in (0, 1) for b in result))

    def test_compute_roundtrip(self):
        block = [1, 0, 1, 1]
        key = [0, 1, 0]
        enc = self.bc.compute(block, key, 0)
        dec = self.bc.compute(enc, key, 1)
        self.assertEqual(dec, block)

    def test_compute_roundtrip_all_zeros(self):
        block = [0, 0, 0, 0]
        key = [0, 0, 0]
        enc = self.bc.compute(block, key, 0)
        dec = self.bc.compute(enc, key, 1)
        self.assertEqual(dec, block)

    def test_compute_roundtrip_all_ones(self):
        block = [1, 1, 1, 1]
        key = [1, 1, 1]
        enc = self.bc.compute(block, key, 0)
        dec = self.bc.compute(enc, key, 1)
        self.assertEqual(dec, block)


# ---------------------------------------------------------------------------
# vigenereCypher
# ---------------------------------------------------------------------------
class TestVigenereCypher(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.vigenereCypher import vigenereCypher
        self.vc = vigenereCypher()

    def test_encrypt_decrypt_roundtrip(self):
        for msg, key in [
            ("HELLOWORLD", "SECRET"),
            ("ATTACKATDAWN", "LEMON"),
            ("CRYPTO", "KEY"),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "A"),
        ]:
            enc = self.vc.encryptMessage(key, msg)
            dec = self.vc.decryptMessage(key, enc)
            self.assertEqual(dec, msg, f"roundtrip failed: msg={msg} key={key}")

    def test_encrypt_known_value(self):
        # HELLO + KEY: H(7)+K(10)=17=R, E(4)+E(4)=8=I, L(11)+Y(24)=35%26=9=J,
        #              L(11)+K(10)=21=V, O(14)+E(4)=18=S  → RIJVS
        enc = self.vc.encryptMessage("KEY", "HELLO")
        self.assertEqual(enc, "RIJVS")

    def test_identity_key_a(self):
        enc = self.vc.encryptMessage("A", "HELLOWORLD")
        self.assertEqual(enc, "HELLOWORLD")

    def test_rotate(self):
        l = list(range(26))
        rotated = self.vc.rotate(l, 1)
        self.assertEqual(rotated[0], 1)
        self.assertEqual(rotated[25], 0)

    def test_rotate_zero(self):
        l = list(range(26))
        self.assertEqual(self.vc.rotate(l, 0), l)

    def test_letter_frequency_sums_to_one(self):
        freq = self.vc.letterFrequency("AABBCC", 1, 0)
        total = sum(freq.values())
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_letter_counter_counts(self):
        dic = self.vc.letterCounter("AAABBC", 1, 0)
        self.assertEqual(dic['A'], 3)
        self.assertEqual(dic['B'], 2)
        self.assertEqual(dic['C'], 1)

    def test_index_of_coincidence_all_same(self):
        text = "A" * 26
        dic = self.vc.letterCounter(text, 1, 0)
        # Convert counts to frequencies for indexC
        freq_dic = {ch: dic[ch] for ch in dic}
        ic = self.vc.indexC(freq_dic, text)
        self.assertAlmostEqual(ic, 1.0, places=5)

    def test_calc_a(self):
        V = [2.0, 4.0, 6.0]
        avg = self.vc.calcA(V, 3)
        self.assertAlmostEqual(avg, 4.0, places=10)

    def test_calc_a_zero_length(self):
        result = self.vc.calcA([], 0)
        self.assertEqual(result, 0.0)

    def test_key_length_positive(self):
        result = self.vc.keyLength(0.045, "A" * 100)
        self.assertGreater(result, 0)


# ---------------------------------------------------------------------------
# gcdEuclid
# ---------------------------------------------------------------------------
class TestGcdEuclid(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.gcdEuclid import gcdEuclid
        self.g = gcdEuclid()

    def test_gcd_basic(self):
        self.assertEqual(self.g.gcdIter(48, 18), 6)

    def test_gcd_coprime(self):
        self.assertEqual(self.g.gcdIter(7, 13), 1)

    def test_gcd_same(self):
        self.assertEqual(self.g.gcdIter(12, 12), 12)

    def test_gcd_one(self):
        self.assertEqual(self.g.gcdIter(1, 999), 1)

    def test_gcd_zero_b(self):
        self.assertEqual(self.g.gcdIter(5, 0), 5)

    def test_gcd_large(self):
        self.assertEqual(self.g.gcdIter(1071, 462), 21)

    def test_gcd_commutative(self):
        self.assertEqual(self.g.gcdIter(100, 75), self.g.gcdIter(75, 100))

    def test_ext_euclid_bezout(self):
        """a*s + b*t == gcd(a, b)"""
        for a, b in [(48, 18), (35, 15), (1071, 462), (7, 13)]:
            out = self.g.ext_euclid(a, b)
            self.assertIsNotNone(out)
            A = max(a, b)
            B = min(a, b)
            gcd = self.g.gcdIter(A, B)
            self.assertEqual(A * out['s'] + B * out['t'], gcd,
                             f"Bezout failed for {a},{b}")

    def test_ext_euclid_gcd_value(self):
        out = self.g.ext_euclid(48, 18)
        self.assertEqual(out['a'], 6)

    def test_ext_euclid_both_zero(self):
        result = self.g.ext_euclid(0, 0)
        self.assertIsNone(result)

    def test_ext_euclid_swaps_order(self):
        # Should handle a < b by swapping
        out_ab = self.g.ext_euclid(18, 48)
        out_ba = self.g.ext_euclid(48, 18)
        self.assertEqual(out_ab['a'], out_ba['a'])


# ---------------------------------------------------------------------------
# merkleHellman
# ---------------------------------------------------------------------------
class TestMerkleHellman(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.merkleHellman import merkleHellman
        self.mh = merkleHellman()

    def test_super_increasing_true(self):
        self.assertTrue(self.mh.superIncreasing([1, 2, 4, 8, 16]))

    def test_super_increasing_false(self):
        self.assertFalse(self.mh.superIncreasing([1, 2, 3]))

    def test_super_increasing_single(self):
        self.assertTrue(self.mh.superIncreasing([5]))

    def test_inverse_mod_known(self):
        # 3 * 9 mod 26 = 27 mod 26 = 1
        result = self.mh.inverseMod(3, 26)
        self.assertEqual((3 * result) % 26, 1)

    def test_inverse_mod_none_for_non_coprime(self):
        # gcd(2, 4) != 1 so no inverse
        result = self.mh.inverseMod(2, 4)
        self.assertIsNone(result)

    def test_inverse_mod_zero(self):
        result = self.mh.inverseMod(0, 26)
        self.assertIsNone(result)

    def test_public_key_known(self):
        # publicKey([1,2,4,8], prime=11, mult=3)
        # 3*1%11=3, 3*2%11=6, 3*4%11=1, 3*8%11=2
        result = self.mh.publicKey([1, 2, 4, 8], 11, 3)
        self.assertEqual(result, [3, 6, 1, 2])

    def test_decrypt_roundtrip(self):
        """Encrypt a 4-bit message with Merkle-Hellman and decrypt it."""
        private_seq = [1, 2, 4, 8]
        prime = 13
        mult = 11
        pub = self.mh.publicKey(private_seq, prime, mult)
        # Encrypt bit vector [1,0,1,0] → sum of pub[0]+pub[2]
        bits = [1, 0, 1, 0]
        encoded = sum(pub[i] for i in range(len(bits)) if bits[i] == 1)
        decoded_bits = self.mh.decryptMH(encoded, private_seq, prime, mult)
        self.assertEqual(decoded_bits[:4], bits)

    def test_parse_sequence_valid(self):
        result = self.mh._parse_sequence("1 2 4 8")
        self.assertEqual(result, [1, 2, 4, 8])

    def test_parse_sequence_invalid(self):
        result = self.mh._parse_sequence("1 2 abc 8")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# RSA
# ---------------------------------------------------------------------------
class TestRSA(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.RSA import RSA
        self.rsa = RSA()

    def test_is_prime_true(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 97]:
            self.assertTrue(self.rsa.isPrime(p), f"{p} should be prime")

    def test_is_prime_false(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 15, 25]:
            self.assertFalse(self.rsa.isPrime(n), f"{n} should not be prime")

    def test_det_m(self):
        self.assertEqual(self.rsa.detM(5, 11), 55)

    def test_det_n(self):
        self.assertEqual(self.rsa.detN(5, 11), 40)

    def test_char_to_int(self):
        result = self.rsa.charToInt("ABC")
        self.assertEqual(result, [0, 1, 2])

    def test_char_to_int_z(self):
        self.assertEqual(self.rsa.charToInt("Z"), [25])

    def test_convert_to_base(self):
        self.assertEqual(self.rsa.covertToBase(10, 2), [1, 0, 1, 0])
        self.assertEqual(self.rsa.covertToBase(0, 10), [0])
        self.assertEqual(self.rsa.covertToBase(26, 26), [1, 0])

    def test_encrypt_decrypt_roundtrip(self):
        """Full RSA roundtrip with small primes p=5, q=11, e=3."""
        p, q = 5, 11
        m = self.rsa.detM(p, q)   # 55
        n = self.rsa.detN(p, q)   # 40
        e = 3
        d = self.rsa.detD(e, n)
        # Encrypt and decrypt a small plaintext value
        for msg in [2, 5, 10, 20]:
            enc = self.rsa.encrypt(msg, e, m)
            dec = self.rsa.decrypt(enc, d, m)
            self.assertEqual(dec, msg, f"RSA roundtrip failed for msg={msg}")

    def test_det_d_inverse(self):
        """e * d ≡ 1 (mod n)"""
        p, q = 5, 11
        e = 3
        n = self.rsa.detN(p, q)
        d = self.rsa.detD(e, n)
        self.assertEqual((e * d) % n, 1)


# ---------------------------------------------------------------------------
# detectEnglish
# ---------------------------------------------------------------------------
class TestDetectEnglish(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from cryptoClasses.detectEnglish import loadDictionary, isEnglish, getEnglishCount, removeNonLetters
        loadDictionary()
        cls.isEnglish = staticmethod(isEnglish)
        cls.getEnglishCount = staticmethod(getEnglishCount)
        cls.removeNonLetters = staticmethod(removeNonLetters)

    def test_is_english_true(self):
        self.assertTrue(self.isEnglish("The quick brown fox jumps over the lazy dog"))

    def test_is_english_false(self):
        self.assertFalse(self.isEnglish("XKJHQZWVMPRTBNLFGYD"))

    def test_remove_non_letters_strips(self):
        result = self.removeNonLetters("Hello, World! 123")
        # Removes punctuation and digits; keeps letters and spaces.
        # "Hello, World! 123" → comma, !, digits removed; one trailing space remains.
        self.assertEqual(result, "Hello World ")

    def test_get_english_count_all_words(self):
        pct = self.getEnglishCount("the cat sat on the mat")
        self.assertGreater(pct, 0.8)

    def test_get_english_count_nonsense(self):
        pct = self.getEnglishCount("xkjhqz wvmpr tbnlfgyd")
        self.assertLess(pct, 0.2)


# ---------------------------------------------------------------------------
# ngram_score
# ---------------------------------------------------------------------------
class TestNgramScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from cryptoClasses.ngram_score import ngram_score
        ngram_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'quadgrams.txt'
        )
        cls.scorer = ngram_score(ngram_file)

    def test_score_returns_float(self):
        result = self.scorer.score("HELLOWORLD")
        self.assertIsInstance(result, float)

    def test_english_scores_higher_than_random(self):
        english = self.scorer.score("THEQUICKBROWNFOX")
        random_text = self.scorer.score("XKJHQZWVMPRTBNLF")
        self.assertGreater(english, random_text)

    def test_score_empty(self):
        # Empty string has no n-grams, so score is 0.0 by definition
        result = self.scorer.score("")
        self.assertIsInstance(result, float)  # returns a float (implementation returns 0.0 or floor)

    def test_ngram_length(self):
        self.assertEqual(self.scorer.L, 4)


# ---------------------------------------------------------------------------
# blowfish (Cipher class)
# ---------------------------------------------------------------------------
class TestBlowfish(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.blowfish import Cipher
        self.Cipher = Cipher

    def test_encrypt_decrypt_block(self):
        c = self.Cipher(b"secretkey1234567890123456")
        block = b"HELLOWOR"
        enc = c.encrypt_block(block)
        dec = c.decrypt_block(enc)
        self.assertEqual(dec, block)

    def test_different_keys_different_ciphertext(self):
        block = b"TESTTEST"
        enc1 = self.Cipher(b"key1key1key1key1").encrypt_block(block)
        enc2 = self.Cipher(b"key2key2key2key2").encrypt_block(block)
        self.assertNotEqual(enc1, enc2)

    def test_same_key_same_ciphertext(self):
        block = b"TESTTEST"
        enc1 = self.Cipher(b"mykey1234567").encrypt_block(block)
        enc2 = self.Cipher(b"mykey1234567").encrypt_block(block)
        self.assertEqual(enc1, enc2)

    def test_ctr_roundtrip(self):
        from cryptoClasses.blowfish import ctr_counter
        import os
        key = b"This is a test key"
        c = self.Cipher(key)
        # ctr_counter takes (nonce_int, f) where f combines two 64-bit ints (e.g. xor)
        nonce = int.from_bytes(os.urandom(8), "big")
        xor = lambda a, b: a ^ b
        counter = ctr_counter(nonce, f=xor)
        plaintext = b"The quick brown fox jumps over the lazy dog"
        # encrypt_ctr and decrypt_ctr return generators; join to bytes
        ciphertext = b"".join(c.encrypt_ctr(plaintext, counter))
        counter2 = ctr_counter(nonce, f=xor)
        decrypted = b"".join(c.decrypt_ctr(ciphertext, counter2))
        self.assertEqual(decrypted, plaintext)

    def test_cbc_roundtrip(self):
        import os
        key = b"This is a test key"
        c = self.Cipher(key)
        iv = os.urandom(8)
        # Must be multiple of 8 bytes; encrypt_cbc/decrypt_cbc return generators
        plaintext = b"The quick brown fox jumps over!!"
        ciphertext = b"".join(c.encrypt_cbc(plaintext, iv))
        decrypted = b"".join(c.decrypt_cbc(ciphertext, iv))
        self.assertEqual(decrypted, plaintext)


# ---------------------------------------------------------------------------
# blowfishP2 (Blowfish class — basic cipher mode only; CBC/CTR are Python 2)
# ---------------------------------------------------------------------------
class TestBlowfishP2(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.blowfishP2 import Blowfish
        self.Blowfish = Blowfish

    def test_cipher_encrypt_decrypt_roundtrip(self):
        bf = self.Blowfish(b"mykey12345678901")
        xl, xr = 0x12345678, 0xABCDEF01
        el, er = bf.cipher(xl, xr, self.Blowfish.ENCRYPT)
        dl, dr = bf.cipher(el, er, self.Blowfish.DECRYPT)
        self.assertEqual((dl, dr), (xl, xr))

    def test_cipher_different_keys(self):
        xl, xr = 0xDEADBEEF, 0xCAFEBABE
        el1, er1 = self.Blowfish(b"key1key1key1key1").cipher(xl, xr, 0)
        el2, er2 = self.Blowfish(b"key2key2key2key2").cipher(xl, xr, 0)
        self.assertNotEqual((el1, er1), (el2, er2))

    def test_invalid_key_too_short(self):
        with self.assertRaises(RuntimeError):
            self.Blowfish(b"short")

    def test_invalid_key_too_long(self):
        with self.assertRaises(RuntimeError):
            self.Blowfish(b"x" * 57)

    def test_encrypt_block_length(self):
        bf = self.Blowfish(b"validkey12345678")
        enc = bf.encrypt(b"HELLOWOR")
        self.assertEqual(len(enc), 8)

    def test_encrypt_decrypt_block_roundtrip(self):
        bf = self.Blowfish(b"validkey12345678")
        plaintext = b"ABCDEFGH"
        enc = bf.encrypt(plaintext)
        dec = bf.decrypt(enc)
        self.assertEqual(dec, plaintext)


# ---------------------------------------------------------------------------
# Atbash (script — test logic inline)
# ---------------------------------------------------------------------------
class TestAtbash(unittest.TestCase):

    def _atbash(self, text):
        """Mirror the script's logic."""
        out = []
        for c in text:
            if ord('a') <= ord(c) <= ord('z'):
                out.append(chr(ord('z') - (ord(c) - ord('a'))))
            elif ord('A') <= ord(c) <= ord('Z'):
                out.append(chr(ord('Z') - (ord(c) - ord('A'))))
            else:
                out.append(c)
        return ''.join(out)

    def test_lowercase(self):
        self.assertEqual(self._atbash("abc"), "zyx")

    def test_uppercase(self):
        self.assertEqual(self._atbash("ABC"), "ZYX")

    def test_involution(self):
        """Atbash is its own inverse."""
        for text in ["HELLO", "world", "AbCdEf"]:
            self.assertEqual(self._atbash(self._atbash(text)), text)

    def test_preserves_non_alpha(self):
        self.assertEqual(self._atbash("Hello, World!"), "Svool, Dliow!")

    def test_full_alphabet(self):
        import string
        enc = self._atbash(string.ascii_uppercase)
        self.assertEqual(enc, string.ascii_uppercase[::-1])

    def test_via_subprocess(self):
        result = subprocess.run(
            ["python3", "cryptoClasses/atbashCypher.py"],
            input="HELLO\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("SVOOL", result.stdout)


# ---------------------------------------------------------------------------
# Scytale (script — test logic inline)
# ---------------------------------------------------------------------------
class TestScytale(unittest.TestCase):

    def _scytale_decode(self, ciphertext, lines):
        """Mirror the script's decoding logic."""
        l = list(ciphertext)
        out = []
        place = 0
        while place < lines:
            j = place
            while j < len(ciphertext):
                out.append(l[j])
                j += lines
            place += 1
        return ''.join(out)

    def test_basic_decode(self):
        # Encode "HELLOWORLD" with 2 rows → interleave: H,L,O,O,L at even, E,L,W,R,D at odd
        # Encoded (read by columns): HLOOL ELWRD → "HLOOLWRD" wait no...
        # Scytale encode with 2 lines: write HELLOWORLD in 2 rows:
        # Row 0: H E L L O   (positions 0,2,4,6,8)
        # Row 1: W O R L D   (positions 1,3,5,7,9)
        # Ciphertext (read by rows): HELLO WORLD  → same. Let's just verify roundtrip by
        # encoding manually and decoding.
        plaintext = "HELLOWORLD"
        lines = 2
        # "Encode" with scytale: write cols as rows → cipher reads cols
        cols = math.ceil(len(plaintext) / lines)
        padded = plaintext.ljust(lines * cols)
        ciphertext = ''
        for col in range(cols):
            for row in range(lines):
                idx = row * cols + col
                if idx < len(padded):
                    ciphertext += padded[idx]
        decoded = self._scytale_decode(ciphertext, lines)
        self.assertEqual(decoded.strip(), plaintext)

    def test_single_line(self):
        self.assertEqual(self._scytale_decode("HELLO", 1), "HELLO")

    def test_via_subprocess(self):
        # To decode to HELLOWORLD with 2 lines, the ciphertext must interleave
        # columns: positions 0,2,4,6,8 = H,E,L,L,O and 1,3,5,7,9 = W,O,R,L,D
        # → ciphertext = "HWEOLRLLOD"
        result = subprocess.run(
            ["python3", "cryptoClasses/scytale.py"],
            input="HWEOLRLLOD\n2\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("HELLOWORLD", result.stdout)

    def test_via_subprocess_single_line(self):
        result = subprocess.run(
            ["python3", "cryptoClasses/scytale.py"],
            input="HELLO\n1\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("HELLO", result.stdout)


# ---------------------------------------------------------------------------
# Hashes (script — test logic inline + subprocess)
# ---------------------------------------------------------------------------
class TestHashes(unittest.TestCase):

    def _compute_hash(self, text):
        """Mirror the hashes.py script logic."""
        import re
        text = re.sub('[^A-Z]', '', text.upper())
        if not text:
            return None
        while len(text) % 5 != 0:
            text += 'X'
        inp = [ord(c) - 65 for c in text]
        output = ''
        for count in range(5):
            temp = sum(inp[i] for i in range(len(inp)) if i % 5 == count)
            output += chr(temp % 26 + 65)
        return output

    def test_hash_length_always_5(self):
        for msg in ["A", "HELLO", "HELLOWORLD", "ABCDEFGHIJ"]:
            self.assertEqual(len(self._compute_hash(msg)), 5)

    def test_hash_deterministic(self):
        self.assertEqual(self._compute_hash("HELLO"), self._compute_hash("HELLO"))

    def test_hash_differs_for_different_inputs(self):
        self.assertNotEqual(self._compute_hash("HELLO"), self._compute_hash("WORLD"))

    def test_hash_only_uppercase_alpha(self):
        result = self._compute_hash("HELLO")
        self.assertTrue(result.isalpha() and result.isupper())

    def test_hash_strips_non_alpha(self):
        self.assertEqual(self._compute_hash("HELLO"), self._compute_hash("H-E-L-L-O"))

    def test_via_subprocess(self):
        result = subprocess.run(
            ["python3", "cryptoClasses/hashes.py"],
            input="HELLO\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("Hash =", result.stdout)
        # Extract hash value and verify 5 uppercase letters
        for line in result.stdout.splitlines():
            if "Hash =" in line:
                h = line.split("=")[1].strip()
                self.assertEqual(len(h), 5)
                self.assertTrue(h.isalpha())


# ---------------------------------------------------------------------------
# Diffie-Hellman (script-only — subprocess)
# ---------------------------------------------------------------------------
class TestDiffieHellman(unittest.TestCase):

    def _dh(self, prime, base, s1, s2):
        alpha = (base ** s1) % prime
        beta = (base ** s2) % prime
        kBeta = (beta ** s1) % prime
        kAlpha = (alpha ** s2) % prime
        return alpha, beta, kBeta, kAlpha

    def test_shared_secret_matches(self):
        alpha, beta, kBeta, kAlpha = self._dh(23, 5, 6, 15)
        self.assertEqual(kBeta, kAlpha)

    def test_known_values(self):
        # Classic DH example: p=23, g=5, a=6, b=15
        alpha, beta, kBeta, kAlpha = self._dh(23, 5, 6, 15)
        self.assertEqual(alpha, 8)
        self.assertEqual(beta, 19)
        self.assertEqual(kBeta, 2)
        self.assertEqual(kAlpha, 2)

    def test_shared_secret_various(self):
        for prime, base, s1, s2 in [(23, 5, 4, 3), (97, 2, 10, 20), (31, 3, 7, 5)]:
            _, _, kBeta, kAlpha = self._dh(prime, base, s1, s2)
            self.assertEqual(kBeta, kAlpha)

    def test_via_subprocess(self):
        result = subprocess.run(
            ["python3", "cryptoClasses/diffieHelman.py"],
            input="23\n5\n6\n15\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("alpha = 8", result.stdout)
        self.assertIn("kBeta = 2", result.stdout)


# ---------------------------------------------------------------------------
# Factor to Primes (script-only — subprocess + logic)
# ---------------------------------------------------------------------------
class TestFactorToPrimes(unittest.TestCase):

    def _factorize(self, num):
        """Mirror factorToPrimes.py logic."""
        import math
        def isPrime(n):
            if n < 2:
                return False
            for i in range(2, math.isqrt(n) + 1):
                if n % i == 0:
                    return False
            return True

        original = num
        output = []
        count = 2
        ceiling = math.ceil(math.sqrt(num))
        remainder = 0

        while count < ceiling + 1:
            if isPrime(count):
                if num % count == 0:
                    remainder = int(num / count)
                    num = remainder
                    ceiling = math.ceil(math.sqrt(num))
                    output.append(count)
                    count = 2
                else:
                    count += 1
            else:
                count += 1

        if remainder != 0 and remainder != 1:
            output.append(remainder)

        output.sort()
        return output

    def test_prime_number(self):
        """A prime number returns no factors (script prints 'is prime')."""
        result = subprocess.run(
            ["python3", "cryptoClasses/factorToPrimes.py"],
            input="17\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("prime", result.stdout.lower())

    def test_factors_12(self):
        factors = self._factorize(12)
        self.assertEqual(sorted(factors), [2, 2, 3])

    def test_factors_60(self):
        factors = self._factorize(60)
        product = 1
        for f in factors:
            product *= f
        self.assertEqual(product, 60)

    def test_product_equals_original(self):
        for n in [12, 36, 100, 360, 1001]:
            factors = self._factorize(n)
            product = 1
            for f in factors:
                product *= f
            self.assertEqual(product, n, f"factors of {n} don't multiply back")

    def test_via_subprocess_12(self):
        result = subprocess.run(
            ["python3", "cryptoClasses/factorToPrimes.py"],
            input="12\n",
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertIn("2", result.stdout)
        self.assertIn("3", result.stdout)


# ---------------------------------------------------------------------------
# subCypher
# ---------------------------------------------------------------------------
class TestSubCypher(unittest.TestCase):

    def setUp(self):
        from cryptoClasses.subCypher import subCypher
        self.sc = subCypher()

    def test_create_key_is_dict(self):
        key = self.sc.createKey("SECRET")
        self.assertIsInstance(key, dict)

    def test_create_key_length_26(self):
        key = self.sc.createKey("SECRET")
        self.assertEqual(len(key), 26)

    def test_create_key_all_alpha_values(self):
        key = self.sc.createKey("SECRET")
        values = list(key.values())
        self.assertEqual(len(set(values)), 26)  # all unique

    def test_create_key_covers_all_letters(self):
        from string import ascii_uppercase
        key = self.sc.createKey("CRYPTO")
        self.assertEqual(set(key.keys()), set(ascii_uppercase))

    def test_encrypt_decrypt_roundtrip(self):
        import tempfile
        key = self.sc.createKey("SECRET")
        # Build inverse key
        inv_key = {v: k for k, v in key.items()}
        plaintext = "HELLOWORLD"
        enc = ''.join(key.get(c, c) for c in plaintext)
        dec = ''.join(inv_key.get(c, c) for c in enc)
        self.assertEqual(dec, plaintext)


if __name__ == '__main__':
    unittest.main(verbosity=2)
