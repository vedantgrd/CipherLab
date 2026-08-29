"""
Full unit test suite for all cipher modules.
Run: python -m pytest tests/ -v
  or: python -m unittest discover -s tests
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from ciphers import caesar, playfair, vigenere, hill, transposition


# ══════════════════════════════════════════════════════════════
#  CAESAR
# ══════════════════════════════════════════════════════════════
class TestCaesar(unittest.TestCase):

    # ── Encryption ────────────────────────────────────────────
    def test_enc_basic(self):             self.assertEqual(caesar.encrypt("HELLO", 3), "KHOOR")
    def test_enc_lowercase(self):         self.assertEqual(caesar.encrypt("hello", 3), "khoor")
    def test_enc_mixed_case(self):        self.assertEqual(caesar.encrypt("Hello", 3), "Khoor")
    def test_enc_spaces_preserved(self):  self.assertEqual(caesar.encrypt("HI THERE", 1), "IJ UIFSF")
    def test_enc_punctuation(self):       self.assertEqual(caesar.encrypt("A,B!", 1), "B,C!")
    def test_enc_wrap_z(self):            self.assertEqual(caesar.encrypt("XYZ", 3), "ABC")
    def test_enc_zero_shift(self):        self.assertEqual(caesar.encrypt("HELLO", 0), "HELLO")
    def test_enc_negative_shift(self):    self.assertEqual(caesar.encrypt("KHOOR", -3), "HELLO")
    def test_enc_large_shift(self):       self.assertEqual(caesar.encrypt("HELLO", 29), "KHOOR")
    def test_enc_full_alphabet(self):
        self.assertEqual(caesar.encrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1),
                         "BCDEFGHIJKLMNOPQRSTUVWXYZA")
    def test_enc_empty(self):             self.assertEqual(caesar.encrypt("", 5), "")
    def test_enc_non_alpha_only(self):    self.assertEqual(caesar.encrypt("123!!", 5), "123!!")

    # ── Decryption ────────────────────────────────────────────
    def test_dec_basic(self):             self.assertEqual(caesar.decrypt("KHOOR", 3), "HELLO")
    def test_dec_empty(self):             self.assertEqual(caesar.decrypt("", 3), "")

    # ── Round trips ───────────────────────────────────────────
    def test_rt_positive(self):
        for k in [1, 7, 13, 25]:
            p = "Hello, World!"
            self.assertEqual(caesar.decrypt(caesar.encrypt(p, k), k), p)

    def test_rt_negative(self):
        p = "TESTING123"
        self.assertEqual(caesar.decrypt(caesar.encrypt(p, -7), -7), p)

    def test_rt_large(self):
        p = "SPHINX"
        self.assertEqual(caesar.decrypt(caesar.encrypt(p, 100), 100), p)

    # ── Steps ─────────────────────────────────────────────────
    def test_steps_count(self):
        s = caesar.steps("HELLO", 3, "encrypt")
        self.assertEqual(len(s), 5)

    def test_steps_alpha_flag(self):
        s = caesar.steps("A!", 1, "encrypt")
        self.assertTrue(s[0]["alpha"])
        self.assertFalse(s[1]["alpha"])

    def test_steps_formula_present(self):
        s = caesar.steps("A", 3, "encrypt")
        self.assertIn("formula", s[0])

    def test_steps_decrypt_mode(self):
        s = caesar.steps("KHOOR", 3, "decrypt")
        self.assertEqual(s[0]["out"], "H")


# ══════════════════════════════════════════════════════════════
#  PLAYFAIR
# ══════════════════════════════════════════════════════════════
class TestPlayfair(unittest.TestCase):

    # ── Matrix ────────────────────────────────────────────────
    def test_matrix_5x5(self):
        m = playfair.build_matrix("MONARCHY")
        self.assertEqual(len(m), 5)
        for row in m: self.assertEqual(len(row), 5)

    def test_matrix_25_unique(self):
        flat = [c for row in playfair.build_matrix("TEST") for c in row]
        self.assertEqual(len(set(flat)), 25)

    def test_matrix_no_j(self):
        flat = [c for row in playfair.build_matrix("JAVA") for c in row]
        self.assertNotIn("J", flat)
        self.assertIn("I", flat)

    def test_matrix_keyword_first(self):
        flat = "".join(c for row in playfair.build_matrix("MONARCHY") for c in row)
        self.assertTrue(flat.startswith("MONAR"))

    # ── Prepare ───────────────────────────────────────────────
    def test_prepare_even_len(self):    self.assertEqual(len(playfair.prepare("HELLO")) % 2, 0)
    def test_prepare_repeated(self):    self.assertIn("X", playfair.prepare("BALLOON"))
    def test_prepare_j_to_i(self):      self.assertNotIn("J", playfair.prepare("JAVA"))
    def test_prepare_odd_padded(self):  self.assertEqual(len(playfair.prepare("ACE")) % 2, 0)

    # ── Encrypt / Decrypt ─────────────────────────────────────
    def test_enc_uppercase(self):
        r = playfair.encrypt("HELLO", "MONARCHY")
        self.assertTrue(r.isupper() and r.isalpha())

    def test_enc_dec_round_trip(self):
        for kw in ["MONARCHY", "SECRET", "KEY"]:
            plain = "HELLOWORLD"
            enc = playfair.encrypt(plain, kw)
            dec = playfair.decrypt(enc, kw)
            self.assertEqual(dec, playfair.prepare(plain))

    def test_ij_equivalence(self):
        self.assertEqual(playfair.encrypt("IIII", "KEY"),
                         playfair.encrypt("JJJJ", "KEY"))

    def test_different_keywords_differ(self):
        self.assertNotEqual(playfair.encrypt("HELLO", "MONARCHY"),
                            playfair.encrypt("HELLO", "SECRET"))

    # ── Steps ─────────────────────────────────────────────────
    def test_steps_has_matrix(self):
        d = playfair.steps("HELLO", "MONARCHY", "encrypt")
        self.assertIn("matrix", d)
        self.assertIn("pairs", d)
        self.assertIn("prepared", d)

    def test_steps_decrypt_has_pairs(self):
        enc = playfair.encrypt("HELLO", "MONARCHY")
        d = playfair.steps(enc, "MONARCHY", "decrypt")
        self.assertIn("pairs", d)
        self.assertTrue(len(d["pairs"]) > 0)


# ══════════════════════════════════════════════════════════════
#  VIGENÈRE
# ══════════════════════════════════════════════════════════════
class TestVigenere(unittest.TestCase):

    # ── Encryption ────────────────────────────────────────────
    def test_known_enc(self):
        self.assertEqual(vigenere.encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_lowercase_preserved(self):
        self.assertEqual(vigenere.encrypt("attackatdawn", "LEMON"), "lxfopvefrnhr")

    def test_spaces_preserved(self):
        r = vigenere.encrypt("HELLO WORLD", "KEY")
        self.assertIn(" ", r)

    def test_punctuation_preserved(self):
        r = vigenere.encrypt("HELLO, WORLD!", "KEY")
        self.assertIn(",", r)
        self.assertIn("!", r)

    def test_key_not_advance_on_space(self):
        r1 = "".join(c for c in vigenere.encrypt("ABCDE", "KEY") if c.isalpha())
        r2 = "".join(c for c in vigenere.encrypt("AB CDE", "KEY") if c.isalpha())
        self.assertEqual(r1, r2)

    def test_empty(self):               self.assertEqual(vigenere.encrypt("", "KEY"), "")

    # ── Decryption ────────────────────────────────────────────
    def test_known_dec(self):
        self.assertEqual(vigenere.decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    # ── Round trips ───────────────────────────────────────────
    def test_rt_various_keys(self):
        for key in ["LEMON", "SECRET", "A", "XYZ"]:
            p = "HELLOWORLD"
            self.assertEqual(vigenere.decrypt(vigenere.encrypt(p, key), key), p)

    def test_rt_with_spaces(self):
        p = "HELLO WORLD"
        self.assertEqual(vigenere.decrypt(vigenere.encrypt(p, "KEY"), "KEY"), p)

    def test_rt_mixed_case(self):
        p = "Hello, World!"
        self.assertEqual(vigenere.decrypt(vigenere.encrypt(p, "Secret"), "Secret"), p)

    # ── Steps ─────────────────────────────────────────────────
    def test_steps_structure(self):
        d = vigenere.steps("ATTACKATDAWN", "LEMON", "encrypt")
        self.assertIn("rows", d)
        self.assertIn("keyword", d)
        self.assertEqual(d["keyword"], "LEMON")

    def test_steps_row_count(self):
        d = vigenere.steps("HELLO", "KEY", "encrypt")
        self.assertEqual(len(d["rows"]), 5)

    def test_steps_non_alpha_flagged(self):
        d = vigenere.steps("A B", "KEY", "encrypt")
        self.assertFalse(d["rows"][1]["alpha"])  # space

    def test_steps_decrypt_mode(self):
        d = vigenere.steps("LXFOPVEFRNHR", "LEMON", "decrypt")
        self.assertEqual(d["mode"], "decrypt")


# ══════════════════════════════════════════════════════════════
#  HILL
# ══════════════════════════════════════════════════════════════
VALID_2 = [[3, 3], [2, 5]]
VALID_3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]


class TestHill(unittest.TestCase):

    # ── Validation ────────────────────────────────────────────
    def test_valid_2x2(self):
        ok, _, _ = hill.validate(VALID_2)
        self.assertTrue(ok)

    def test_valid_3x3(self):
        ok, _, _ = hill.validate(VALID_3)
        self.assertTrue(ok)

    def test_singular(self):
        ok, msg, _ = hill.validate([[1, 2], [2, 4]])
        self.assertFalse(ok)
        self.assertTrue(len(msg) > 0)  # invalid matrix produces error

    def test_gcd_not_one(self):
        ok, _, _ = hill.validate([[2, 1], [4, 5]])  # det=6, gcd(6,26)=2
        self.assertFalse(ok)

    def test_all_zeros(self):
        ok, _, _ = hill.validate([[0, 0], [0, 0]])
        self.assertFalse(ok)

    # ── Encryption ────────────────────────────────────────────
    def test_enc_known_he(self):
        # H(7),E(4): [3*7+3*4, 2*7+5*4]=[33,34] mod26=[7,8] → H,I
        self.assertEqual(hill.encrypt("HE", VALID_2), "HI")

    def test_enc_output_alpha_upper(self):
        r = hill.encrypt("HELP", VALID_2)
        self.assertTrue(r.isupper() and r.isalpha())

    def test_enc_padding(self):
        r = hill.encrypt("HEL", VALID_2)
        self.assertEqual(len(r), 4)  # HELX padded

    def test_enc_invalid_raises(self):
        with self.assertRaises(ValueError):
            hill.encrypt("HELLO", [[1, 2], [2, 4]])

    def test_enc_3x3_length(self):
        r = hill.encrypt("ABCDEF", VALID_3)
        self.assertEqual(len(r), 6)

    # ── Decryption ────────────────────────────────────────────
    def test_dec_known(self):
        self.assertEqual(hill.decrypt("HI", VALID_2), "HE")

    def test_dec_invalid_raises(self):
        with self.assertRaises(ValueError):
            hill.decrypt("ABCD", [[1, 2], [2, 4]])

    # ── Round trips ───────────────────────────────────────────
    def test_rt_2x2(self):
        self.assertEqual(hill.decrypt(hill.encrypt("HELP", VALID_2), VALID_2), "HELP")

    def test_rt_3x3(self):
        self.assertEqual(hill.decrypt(hill.encrypt("ABCDEF", VALID_3), VALID_3), "ABCDEF")

    def test_rt_padding(self):
        # HEL → padded to HELX on encrypt, decrypt gives HELX back
        self.assertEqual(hill.decrypt(hill.encrypt("HEL", VALID_2), VALID_2), "HELX")

    # ── Steps ─────────────────────────────────────────────────
    def test_steps_structure(self):
        d = hill.steps("HELP", VALID_2, "encrypt")
        self.assertIn("blocks", d)
        self.assertIn("matrix", d)
        self.assertIn("padded", d)
        self.assertIn("n", d)

    def test_steps_block_count(self):
        d = hill.steps("HELP", VALID_2, "encrypt")
        self.assertEqual(len(d["blocks"]), 2)

    def test_steps_decrypt_uses_inverse(self):
        d = hill.steps("HI", VALID_2, "decrypt")
        self.assertNotEqual(d["matrix"], VALID_2)

    def test_steps_3x3(self):
        d = hill.steps("ABCDEF", VALID_3, "encrypt")
        self.assertEqual(d["n"], 3)
        self.assertEqual(len(d["blocks"]), 2)


# ══════════════════════════════════════════════════════════════
#  TRANSPOSITION
# ══════════════════════════════════════════════════════════════
class TestTransposition(unittest.TestCase):

    # ── Column order ──────────────────────────────────────────
    def test_order_all_ranks(self):
        order = transposition.col_order("ZEBRAS")
        self.assertEqual(sorted(order), list(range(6)))

    def test_order_a_rank_0(self):
        order = transposition.col_order("ZEBRAS")
        self.assertEqual(order[4], 0)  # A at index 4 → rank 0

    def test_order_z_last(self):
        order = transposition.col_order("ZEBRAS")
        self.assertEqual(order[0], 5)  # Z at index 0 → rank 5

    def test_order_duplicates_by_position(self):
        order = transposition.col_order("AABB")
        self.assertEqual(order[0], 0)  # first A → rank 0
        self.assertEqual(order[1], 1)  # second A → rank 1
        self.assertEqual(order[2], 2)  # first B → rank 2
        self.assertEqual(order[3], 3)  # second B → rank 3

    def test_order_single(self):
        self.assertEqual(transposition.col_order("A"), [0])

    # ── Encryption ────────────────────────────────────────────
    def test_enc_length_divisible(self):
        r = transposition.encrypt("WEAREDISCOVEREDFLEEATONCE", "ZEBRAS")
        self.assertEqual(len(r) % 6, 0)

    def test_enc_single_key(self):
        self.assertEqual(transposition.encrypt("HELLO", "A"), "HELLO")

    def test_enc_duplicate_key(self):
        r = transposition.encrypt("HELLOWORLD", "AABB")
        self.assertIsInstance(r, str)

    def test_enc_chars_preserved(self):
        from collections import Counter
        text = "HELLOWORLD"
        r = transposition.encrypt(text, "KEY")
        for ch in text:
            self.assertGreaterEqual(Counter(r)[ch], Counter(text)[ch])

    # ── Decryption ────────────────────────────────────────────
    def test_dec_round_trip_zebras(self):
        text = "WEAREDISCOVEREDFLEEATONCE"
        enc = transposition.encrypt(text, "ZEBRAS")
        dec = transposition.decrypt(enc, "ZEBRAS")
        self.assertTrue(dec.startswith(text))

    def test_dec_round_trip_keys(self):
        for key in ["KEY", "SECRET", "AB", "AABB", "CRYPTO"]:
            text = "HELLOWORLD"
            enc = transposition.encrypt(text, key)
            dec = transposition.decrypt(enc, key)
            self.assertTrue(dec.startswith(text), f"Failed key={key}")

    def test_dec_single_key(self):
        self.assertEqual(transposition.decrypt("HELLO", "A"), "HELLO")

    def test_dec_invalid_length_raises(self):
        with self.assertRaises(ValueError):
            transposition.decrypt("ABCDE", "KEY")  # 5 not divisible by 3

    # ── Steps ─────────────────────────────────────────────────
    def test_steps_enc_structure(self):
        d = transposition.steps("HELLOWORLD", "KEY", "encrypt")
        self.assertIn("grid", d)
        self.assertIn("colReads", d)
        self.assertIn("order", d)
        self.assertIn("result", d)
        self.assertIn("keyword", d)

    def test_steps_enc_grid_shape(self):
        d = transposition.steps("HELLOWORLD", "KEY", "encrypt")
        self.assertEqual(d["nRows"], 4)        # 10 chars padded to 12, 12/3=4 rows
        self.assertEqual(len(d["grid"]), 4)
        for row in d["grid"]:
            self.assertEqual(len(row), 3)

    def test_steps_dec_structure(self):
        enc = transposition.encrypt("HELLOWORLD", "KEY")
        d = transposition.steps(enc, "KEY", "decrypt")
        self.assertIn("colReads", d)
        self.assertIn("result", d)

    def test_steps_result_matches_encrypt(self):
        text = "HELLOWORLD"
        key = "ZEBRAS"
        enc = transposition.encrypt(text, key)
        d = transposition.steps(text, key, "encrypt")
        self.assertEqual(d["result"], enc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
