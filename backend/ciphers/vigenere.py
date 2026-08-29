"""Vigenère Cipher — polyalphabetic substitution."""


def _stream(text, kw):
    kw = kw.upper(); ki = 0; s = []
    for c in text:
        if c.isalpha(): s.append(kw[ki % len(kw)]); ki += 1
        else: s.append(None)
    return s


def encrypt(text: str, keyword: str) -> str:
    stream = _stream(text, keyword)
    out = []
    for c, k in zip(text, stream):
        if c.isalpha() and k:
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c)-base + ord(k)-65) % 26 + base))
        else: out.append(c)
    return ''.join(out)


def decrypt(text: str, keyword: str) -> str:
    stream = _stream(text, keyword)
    out = []
    for c, k in zip(text, stream):
        if c.isalpha() and k:
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c)-base - (ord(k)-65)) % 26 + base))
        else: out.append(c)
    return ''.join(out)


def steps(text: str, keyword: str, mode: str) -> dict:
    stream = _stream(text, keyword)
    rows = []
    for c, k in zip(text, stream):
        if c.isalpha() and k:
            p = ord(c.upper())-65; s = ord(k)-65
            q = (p+s if mode=='encrypt' else p-s) % 26
            rows.append({"plain": c.upper(), "key": k,
                         "cipher": chr(q+65),
                         "formula": f"({p}{'+'if mode=='encrypt' else'-'}{s}) mod 26={q}",
                         "alpha": True})
        else:
            rows.append({"plain": c, "key": "-", "cipher": c, "alpha": False})
    return {"rows": rows, "keyword": keyword.upper(), "mode": mode}
