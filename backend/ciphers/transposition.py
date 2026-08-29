"""Columnar Transposition Cipher."""


def col_order(keyword: str) -> list:
    kw = keyword.upper()
    idx = sorted(enumerate(kw), key=lambda x: (x[1], x[0]))
    order = [0]*len(kw)
    for rank,(orig,_) in enumerate(idx): order[orig] = rank
    return order

def _rtc(keyword):
    order = col_order(keyword); n = len(order)
    result = [0]*n
    for col,rank in enumerate(order): result[rank] = col
    return result

def encrypt(text, keyword):
    keyword = keyword.upper(); n = len(keyword)
    text = text.replace('\n','').replace('\r','')
    while len(text)%n: text += 'X'
    nr = len(text)//n
    grid = [list(text[r*n:(r+1)*n]) for r in range(nr)]
    rtc = _rtc(keyword)
    return ''.join(grid[r][rtc[rank]] for rank in range(n) for r in range(nr))

def decrypt(text, keyword):
    keyword = keyword.upper(); n = len(keyword)
    if len(text)%n: raise ValueError(f"Ciphertext length {len(text)} not divisible by key length {n}.")
    nr = len(text)//n; rtc = _rtc(keyword)
    cols = {}; pos = 0
    for rank in range(n):
        cols[rtc[rank]] = list(text[pos:pos+nr]); pos += nr
    return ''.join(cols[c][r] for r in range(nr) for c in range(n))

def steps(text, keyword, mode):
    keyword = keyword.upper(); n = len(keyword)
    order = col_order(keyword); rtc = _rtc(keyword)
    if mode == 'encrypt':
        padded = text.replace('\n','').replace('\r','')
        while len(padded)%n: padded += 'X'
        nr = len(padded)//n
        grid = [list(padded[r*n:(r+1)*n]) for r in range(nr)]
        col_reads = []
        for rank in range(n):
            col = rtc[rank]
            col_reads.append({"rank":rank,"col":col,"letter":keyword[col],
                               "chars":''.join(grid[r][col] for r in range(nr))})
        result = ''.join(cr["chars"] for cr in col_reads)
        return {"keyword":keyword,"order":order,"grid":grid,
                "colReads":col_reads,"result":result,"nRows":nr,"mode":mode}
    else:
        nr = len(text)//n; cols = {}; pos = 0
        col_reads = []
        for rank in range(n):
            col = rtc[rank]; chunk = text[pos:pos+nr]
            cols[col] = list(chunk)
            col_reads.append({"rank":rank,"col":col,"letter":keyword[col],"chars":chunk})
            pos += nr
        grid = [[cols[c][r] for c in range(n)] for r in range(nr)]
        result = ''.join(cols[c][r] for r in range(nr) for c in range(n))
        return {"keyword":keyword,"order":order,"grid":grid,
                "colReads":col_reads,"result":result,"nRows":nr,"mode":mode}
