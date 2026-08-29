"""Hill Cipher — matrix multiplication mod 26."""
import math


def _det2(m): return m[0][0]*m[1][1] - m[0][1]*m[1][0]
def _det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
           -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
           +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))

def _adj2(m): return [[m[1][1],-m[0][1]],[-m[1][0],m[0][0]]]
def _adj3(m):
    cf = [[ (m[1][1]*m[2][2]-m[1][2]*m[2][1]),-(m[1][0]*m[2][2]-m[1][2]*m[2][0]),(m[1][0]*m[2][1]-m[1][1]*m[2][0])],
          [-(m[0][1]*m[2][2]-m[0][2]*m[2][1]), (m[0][0]*m[2][2]-m[0][2]*m[2][0]),-(m[0][0]*m[2][1]-m[0][1]*m[2][0])],
          [ (m[0][1]*m[1][2]-m[0][2]*m[1][1]),-(m[0][0]*m[1][2]-m[0][2]*m[1][0]),(m[0][0]*m[1][1]-m[0][1]*m[1][0])]]
    return [[cf[j][i] for j in range(3)] for i in range(3)]

def _modinv(a, m=26):
    a %= m
    for x in range(1, m):
        if (a*x)%m == 1: return x
    raise ValueError(f"No inverse for {a} mod {m}")

def validate(matrix):
    n = len(matrix)
    d = _det2(matrix) if n==2 else _det3(matrix)
    dm = d % 26; g = math.gcd(dm, 26)
    if dm==0 or g!=1:
        return False, f"det={d} ≡ {dm} (mod 26), gcd({dm},26)={g} ≠ 1", dm
    return True, f"det={d} ≡ {dm} (mod 26), gcd({dm},26)=1 ✓", dm

def _inverse(matrix):
    n = len(matrix)
    d = _det2(matrix) if n==2 else _det3(matrix)
    di = _modinv(d % 26)
    adj = _adj2(matrix) if n==2 else _adj3(matrix)
    return [[(di*adj[i][j])%26 for j in range(n)] for i in range(n)]

def _mv(mat, vec):
    n = len(mat)
    return [sum(mat[i][j]*vec[j] for j in range(n))%26 for i in range(n)]

def _vecs(text, n):
    chars = [c.upper() for c in text if c.isalpha()]
    while len(chars)%n: chars.append('X')
    return [[ord(chars[i+j])-65 for j in range(n)] for i in range(0,len(chars),n)], ''.join(chars)

def encrypt(text, matrix):
    ok,msg,_ = validate(matrix)
    if not ok: raise ValueError(msg)
    n = len(matrix); vecs,_ = _vecs(text,n)
    return ''.join(chr(v+65) for vec in vecs for v in _mv(matrix,vec))

def decrypt(text, matrix):
    ok,msg,_ = validate(matrix)
    if not ok: raise ValueError(msg)
    inv = _inverse(matrix); n = len(inv)
    vecs,_ = _vecs(text,n)
    return ''.join(chr(v+65) for vec in vecs for v in _mv(inv,vec))

def steps(text, matrix, mode):
    n = len(matrix)
    op = _inverse(matrix) if mode=='decrypt' else matrix
    vecs, padded = _vecs(text, n)
    blocks = []
    for i, vec in enumerate(vecs):
        out_vec = _mv(op, vec)
        detail = []
        for r in range(n):
            terms = ' + '.join(f"{op[r][c]}×{vec[c]}" for c in range(n))
            total = sum(op[r][c]*vec[c] for c in range(n))
            detail.append(f"{terms} = {total} → {total%26}")
        blocks.append({"input": padded[i*n:(i+1)*n], "vec": vec,
                       "outVec": out_vec, "output": ''.join(chr(v+65) for v in out_vec),
                       "detail": detail})
    ok, valid_msg, _ = validate(matrix)
    return {"matrix": op, "origMatrix": matrix, "blocks": blocks,
            "padded": padded, "mode": mode, "n": n, "validMsg": valid_msg}
