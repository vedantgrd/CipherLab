"""Caesar Cipher — monoalphabetic substitution."""


def encrypt(text: str, shift: int) -> str:
    shift = shift % 26
    return ''.join(
        chr((ord(c) - (65 if c.isupper() else 97) + shift) % 26
            + (65 if c.isupper() else 97)) if c.isalpha() else c
        for c in text
    )


def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)


def steps(text: str, shift: int, mode: str) -> list:
    actual = (shift if mode == 'encrypt' else -shift) % 26
    out = []
    for c in text:
        if c.isalpha():
            base = 65 if c.isupper() else 97
            p = ord(c) - base
            q = (p + actual) % 26
            out.append({"in": c, "out": chr(q + base),
                        "formula": f"({p}+{actual}) mod 26 = {q}", "alpha": True})
        else:
            out.append({"in": c, "out": c, "alpha": False})
    return out
