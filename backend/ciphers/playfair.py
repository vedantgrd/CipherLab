"""Playfair Cipher — 5×5 digraph substitution."""


def build_matrix(keyword: str) -> list:
    kw = keyword.upper().replace('J', 'I')
    seen, letters = set(), []
    for c in kw:
        if c.isalpha() and c not in seen:
            seen.add(c); letters.append(c)
    for c in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if c not in seen:
            seen.add(c); letters.append(c)
    return [letters[i*5:(i+1)*5] for i in range(5)]


def _pos(m, c):
    c = c.upper().replace('J', 'I')
    for r, row in enumerate(m):
        for col, ch in enumerate(row):
            if ch == c: return r, col
    raise ValueError(f"'{c}' not in matrix")


def prepare(text: str) -> str:
    t = [c for c in text.upper().replace('J','I') if c.isalpha()]
    res, i = [], 0
    while i < len(t):
        a = t[i]
        if i+1 < len(t):
            b = t[i+1]
            if a == b: res += [a, 'X']; i += 1
            else: res += [a, b]; i += 2
        else: res += [a, 'X']; i += 1
    return ''.join(res)


def encrypt(text: str, keyword: str) -> str:
    m = build_matrix(keyword)
    prep = prepare(text)
    out = []
    for i in range(0, len(prep), 2):
        a, b = prep[i], prep[i+1]
        r1,c1 = _pos(m,a); r2,c2 = _pos(m,b)
        if r1==r2:   out += [m[r1][(c1+1)%5], m[r2][(c2+1)%5]]
        elif c1==c2: out += [m[(r1+1)%5][c1], m[(r2+1)%5][c2]]
        else:        out += [m[r1][c2], m[r2][c1]]
    return ''.join(out)


def decrypt(text: str, keyword: str) -> str:
    m = build_matrix(keyword)
    t = [c for c in text.upper().replace('J','I') if c.isalpha()]
    if len(t)%2: t.append('X')
    out = []
    for i in range(0, len(t), 2):
        a, b = t[i], t[i+1]
        r1,c1 = _pos(m,a); r2,c2 = _pos(m,b)
        if r1==r2:   out += [m[r1][(c1-1)%5], m[r2][(c2-1)%5]]
        elif c1==c2: out += [m[(r1-1)%5][c1], m[(r2-1)%5][c2]]
        else:        out += [m[r1][c2], m[r2][c1]]
    return ''.join(out)


def steps(text: str, keyword: str, mode: str) -> dict:
    m = build_matrix(keyword)
    kw_chars = set(keyword.upper().replace('J','I'))
    if mode == 'encrypt':
        prep = prepare(text)
        pairs = []
        for i in range(0, len(prep), 2):
            a,b = prep[i], prep[i+1]
            r1,c1=_pos(m,a); r2,c2=_pos(m,b)
            if r1==r2:
                ea,eb = m[r1][(c1+1)%5], m[r2][(c2+1)%5]
                rule = "Same Row → shift right"
            elif c1==c2:
                ea,eb = m[(r1+1)%5][c1], m[(r2+1)%5][c2]
                rule = "Same Col → shift down"
            else:
                ea,eb = m[r1][c2], m[r2][c1]
                rule = "Rectangle → swap cols"
            pairs.append({"in": a+b, "out": ea+eb, "rule": rule})
        return {"matrix": m, "kwChars": list(kw_chars), "prepared": prep,
                "pairs": pairs, "mode": mode}
    else:
        t = [c for c in text.upper().replace('J','I') if c.isalpha()]
        if len(t)%2: t.append('X')
        pairs = []
        for i in range(0, len(t), 2):
            a,b = t[i], t[i+1]
            r1,c1=_pos(m,a); r2,c2=_pos(m,b)
            if r1==r2:
                da,db = m[r1][(c1-1)%5], m[r2][(c2-1)%5]
                rule = "Same Row → shift left"
            elif c1==c2:
                da,db = m[(r1-1)%5][c1], m[(r2-1)%5][c2]
                rule = "Same Col → shift up"
            else:
                da,db = m[r1][c2], m[r2][c1]
                rule = "Rectangle → swap cols"
            pairs.append({"in": a+b, "out": da+db, "rule": rule})
        return {"matrix": m, "kwChars": list(kw_chars), "pairs": pairs, "mode": mode}
